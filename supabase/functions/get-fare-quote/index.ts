import "@supabase/functions-js/edge-runtime.d.ts";
import { withSupabase } from "@supabase/server";

const GOOGLE_MAPS_SERVER_KEY = Deno.env.get("GOOGLE_MAPS_SERVER_KEY")!;

export default {
  fetch: withSupabase({ auth: 'user' }, async (req, ctx) => {
    try {
      const user = ctx.userClaims;
      if (!user) {
        return Response.json({ error: "Not signed in" }, { status: 401 });
      }

      const { pickup_address, dropoff_address, vehicle_type, addon_ids, load_weight_kg } = await req.json();

      if (!pickup_address || !dropoff_address || !vehicle_type) {
        return Response.json({ error: "Missing required fields" }, { status: 400 });
      }

      const { data: vehicle, error: vehicleErr } = await ctx.supabaseAdmin
        .from("vehicle_types")
        .select("base_price, per_km_rate")
        .eq("name", vehicle_type)
        .eq("active", true)
        .single();

      if (vehicleErr || !vehicle) {
        return Response.json({ error: "Unknown vehicle type" }, { status: 400 });
      }

      const dmUrl = new URL("https://maps.googleapis.com/maps/api/distancematrix/json");
      dmUrl.searchParams.set("origins", pickup_address);
      dmUrl.searchParams.set("destinations", dropoff_address);
      dmUrl.searchParams.set("key", GOOGLE_MAPS_SERVER_KEY);

      const dmRes = await fetch(dmUrl.toString());
      const dmData = await dmRes.json();

      const element = dmData?.rows?.[0]?.elements?.[0];
      if (!element || element.status !== "OK") {
        return Response.json({ error: "Could not calculate distance for these addresses" }, { status: 422 });
      }

      const distanceKm = element.distance.value / 1000;

      const baseFee = Number(vehicle.base_price);
      const perKmRate = Number(vehicle.per_km_rate);
      const distanceFee = Math.round(distanceKm * perKmRate);

      let addonsTotal = 0;
      if (Array.isArray(addon_ids) && addon_ids.length > 0) {
        const { data: addons, error: addonsErr } = await ctx.supabaseAdmin
          .from("service_addons")
          .select("id, price")
          .in("id", addon_ids)
          .eq("active", true);

        if (addonsErr) {
          return Response.json({ error: "Could not price add-ons" }, { status: 500 });
        }
        addonsTotal = (addons ?? []).reduce((sum, a) => sum + Number(a.price), 0);
      }

      let loadSurcharge = 0;
      if (load_weight_kg != null) {
        const { data: tier, error: tierErr } = await ctx.supabaseAdmin
          .from("load_tiers")
          .select("surcharge_amount, min_weight_kg, max_weight_kg")
          .eq("active", true)
          .lte("min_weight_kg", load_weight_kg)
          .order("sort_order")
          .limit(1)
          .maybeSingle();

        if (tierErr) {
          return Response.json({ error: "Could not price load surcharge" }, { status: 500 });
        }
        if (tier && (tier.max_weight_kg == null || load_weight_kg <= tier.max_weight_kg)) {
          loadSurcharge = Number(tier.surcharge_amount);
        }
      }

      const totalFare = Math.round(baseFee + distanceFee + addonsTotal + loadSurcharge);

      const expiresAt = new Date(Date.now() + 10 * 60 * 1000).toISOString();

      const { data: quote, error: insertErr } = await ctx.supabaseAdmin
        .from("fare_quotes")
        .insert({
          rider_id: user.id,
          pickup_address,
          dropoff_address,
          vehicle_type,
          distance_km: distanceKm,
          base_fee: baseFee,
          distance_fee: distanceFee,
          addons_total: addonsTotal,
          load_weight_kg: load_weight_kg ?? null,
          load_surcharge_amount: loadSurcharge,
          total_fare: totalFare,
          expires_at: expiresAt,
        })
        .select("id")
        .single();

      if (insertErr || !quote) {
        console.error("Failed to store fare quote", insertErr);
        return Response.json({ error: "Could not generate quote" }, { status: 500 });
      }

      return Response.json({
        quote_id: quote.id,
        distance_km: Math.round(distanceKm * 10) / 10,
        base_fee: baseFee,
        distance_fee: distanceFee,
        addons_total: addonsTotal,
        load_surcharge_amount: loadSurcharge,
        total_fare: totalFare,
        expires_at: expiresAt,
      });
    } catch (e) {
      console.error("get-fare-quote error", e);
      return Response.json({ error: "Internal error" }, { status: 500 });
    }
  }),
};
