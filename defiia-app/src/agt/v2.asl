// initial belief, given by the developer
preferred_temp(20).

// reaction to changes in the temperature
+temperature(T)  : preferred_temp(P) & math.abs(P-T) > 2
   <- !temperature(P).
+temperature(T)  : preferred_temp(T)
   <- turn_off(ac).

// plans to achieve some temperature
+!temperature(P) : temperature(T) & T >  P
   <- turn_on(ac).

{ include("$jacamoJar/templates/common-cartago.asl") }
{ include("$jacamoJar/templates/common-moise.asl") }

// features:
//
//  - selection of plans based on context
