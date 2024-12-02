

+temperature(30)  <- !temperature(20).
+temperature(20)  <- turn_off(ac).

+!temperature(20) <- turn_on(ac).

{ include("$jacamoJar/templates/common-cartago.asl") }
{ include("$jacamoJar/templates/common-moise.asl") }

// features:
//
//  - reactivity (to changes in temp)
//    (event oriented)
//  - pro-activity (creation of new goals)
//
//  - not a conventional program, but a set of plans
//    the agent selects
