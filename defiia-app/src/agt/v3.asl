// initial belief, given by the developer
preferred_temp(20).

// initial goal, given by the developer
!keep_temperature.

// maintenance the goal pattern
+!keep_temperature
    : temperature(T) & preferred_temp(P) & T >  P
   <- turn_on(ac); .wait(500);
      !keep_temperature.
+!keep_temperature
    : temperature(T) & preferred_temp(P) & T <= P
   <- turn_off(ac); .wait(500);
      !keep_temperature.

{ include("$jacamoJar/templates/common-cartago.asl") }
{ include("$jacamoJar/templates/common-moise.asl") }

// features:
//  - goal oriented (maintenance goal)
