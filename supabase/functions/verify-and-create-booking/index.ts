import { createClient } from "https://esm.sh/@supabase/supabase-js@2";

const FARE_TOLERANCE_RAND = 2;

Deno.serve(async (req) => {
  if (req.method === "OPTIONS") {
    return new Response("ok", {
      headers: {
        "Access-Control-Allow-Origin": "*",
        "Access-Control-Allow-Headers": "authorization, apikey, content-type",
      },
    });
  }
  try {
    const authHeader = req.headers.get("Authorization") || "";
    const userClient = createClient(
      Deno.env.get("SUPABASE_URL")!,
      Deno.env.get("SUPABASE_ANON_KEY")!,
      { global: { headers: { Authorization: authHeader } } },
    );
    const { data: userData, error: userErr } = await userClient.auth.getUser();
    if (userErr || !userData.user) {
      return Response.json({ error: "Not signed in" }, { status: 401 });
    }
    const user = userData.user;
    const {
      pickup_address,
      pickup_lat,
      pickup_lng,
      dropoff_address,
      dropoff_lat,
      dropoff_lng,
      vehicle_type_id,
      addon_ids,
      load_weight_kg,
      claimed_total_fare,
      paystack_reference,
    } = await req.json();

    if (!pickup_address || !dropoff_address || !vehicle_type_id) {
      return Response.json({ error: "Missing required fields" }, { status: 400 });
    }

    const admin = createClient(
      Deno.env.get("SUPABASE_URL")!,
      Deno.env.get("SUPABASE_SERVICE_ROLE_KEY")!,
    );

    const { data: vehicle, error: vehicleErr } = await admin
      .from("vehicle_types")
      .select("id, name, base_price, per_km_rate, active")
      .eq("id", vehicle_type_id)
      .single();
    if (vehicleErr || !vehicle || !vehicle.active) {
      return Response.json({ error: "Invalid or inactive vehicle type" }, { status: 400 });
    }

    let addonsTotal = 0;
    let addonsData: { id: string; name: string; price: number }[] = [];
    if (Array.isArray(addon_ids) && addon_ids.length > 0) {
      const { data: addons, error: addonsErr } = await admin
        .from("service_addons")
        .select("id, name, price")
        .in("id", addon_ids)
        .eq("active", true);
      if (addonsErr) return Response.json({ error: "Could not verify add-ons" }, { status: 500 });
      addonsData = addons || [];
      addonsTotal = addonsData.reduce((sum, a) => sum + Number(a.price), 0);
    }

    let loadSurcharge = 0;
    if (load_weight_kg != null) {
      const { data: tier } = await admin
        .from("load_tiers")
        .select("surcharge_amount, min_weight_kg, max_weight_kg")
        .eq("active", true)
        .lte("min_weight_kg", load_weight_kg)
        .order("sort_order")
        .limit(1)
        .maybeSingle();
      if (tier && (tier.max_weight_kg == null || load_weight_kg <= tier.max_weight_kg)) {
        loadSurcharge = Number(tier.surcharge_amount);
      }
    }

    const mapsKey = Deno.env.get("GOOGLE_MAPS_SERVER_KEY");
    if (!mapsKey) return Response.json({ error: "Maps key missing" }, { status: 500 });
    const dmUrl = new URL("https://maps.googleapis.com/maps/api/distancematrix/json");
    dmUrl.searchParams.set("origins", pickup_address);
    dmUrl.searchParams.set("destinations", dropoff_address);
    dmUrl.searchParams.set("key", mapsKey);
    const dmData = await fetch(dmUrl.toString()).then((r) => r.json());
    const element = dmData?.rows?.[0]?.elements?.[0];
    if (!element || element.status !== "OK") {
      return Response.json({ error: "Could not calculate distance for these addresses" }, { status: 422 });
    }

    const distanceKm = element.distance.value / 1000;
    const basePrice = Number(vehicle.base_price);
    const perKmRate = Number(vehicle.per_km_rate);
    const distanceFee = Math.round(distanceKm * perKmRate);
    const realTotalFare = Math.round(basePrice + distanceFee + addonsTotal + loadSurcharge);

    if (typeof claimed_total_fare === "number" && Math.abs(claimed_total_fare - realTotalFare) > FARE_TOLERANCE_RAND) {
      return Response.json({ error: "Fare mismatch detected", expected_total_fare: realTotalFare }, { status: 409 });
    }

    const expiresAt = new Date(Date.now() + 10 * 60 * 1000).toISOString();
    const { data: quote, error: quoteErr } = await admin.from("fare_quotes").insert({
      rider_id: user.id,
      pickup_address,
      dropoff_address,
      vehicle_type: vehicle.name,
      distance_km: distanceKm,
      base_fee: basePrice,
      distance_fee: distanceFee,
      addons_total: addonsTotal,
      load_weight_kg: load_weight_kg ?? null,
      load_surcharge_amount: loadSurcharge,
      total_fare: realTotalFare,
      expires_at: expiresAt,
    }).select("id").single();
    if (quoteErr || !quote) return Response.json({ error: "Could not lock fare" }, { status: 500 });

    const { data: booking, error: insertErr } = await admin.from("bookings").insert({
      rider_id: user.id,
      quote_id: quote.id,
      pickup_address,
      pickup_lat: pickup_lat ?? null,
      pickup_lng: pickup_lng ?? null,
      dropoff_address,
      dropoff_lat: dropoff_lat ?? null,
      dropoff_lng: dropoff_lng ?? null,
      vehicle_type_id: vehicle.id,
      vehicle_name: vehicle.name,
      base_fare: basePrice,
      total_fare: realTotalFare,
      addons: addonsData.map((a) => ({ name: a.name, price: a.price })),
      addons_total: addonsTotal,
      load_weight_kg: load_weight_kg ?? null,
      status: "pending",
      paystack_reference: paystack_reference || null,
      payout_status: paystack_reference ? "paid" : "unpaid",
    }).select().single();
    if (insertErr || !booking) return Response.json({ error: insertErr?.message || "Could not create booking" }, { status: 500 });

    return Response.json({
      booking,
      distance_km: Math.round(distanceKm * 10) / 10,
      total_fare: realTotalFare,
    });
  } catch (e) {
    return Response.json({ error: String(e) }, { status: 500 });
  }
});
