/// initial belief, given by the developer
preferred_temp(20).

// initial goal, given by the developer
!keep_temperature.

// maintenance the goal pattern
+!keep_temperature
    : temperature(T) & preferred_temp(P) & T >  P &
      state("off")
   <- turn_on(ac);
      !keep_temperature.
+!keep_temperature
    : temperature(T) & preferred_temp(P) & T <= P &
      state("on")
   <- turn_off(ac);
      !keep_temperature.
+!keep_temperature
   <- .wait(500);
      !keep_temperature.

{ include("$jacamoJar/templates/common-cartago.asl") }
{ include("$jacamoJar/templates/common-moise.asl") }
