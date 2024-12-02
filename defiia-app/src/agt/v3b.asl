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

+!keep_temperature
   <- .wait(500);
      !keep_temperature.

+!stop
   <- turn_off(ac);
      .drop_intention(keep_temperature).

{ include("$jacamoJar/templates/common-cartago.asl") }
{ include("$jacamoJar/templates/common-moise.asl") }
