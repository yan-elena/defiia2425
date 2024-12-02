!send_msgs.

+!send_msgs
   <- .send(rc,tell,preferred_temp(25));
      .wait(3000);
      .send(rc,untell,preferred_temp(25));
      .send(rc,tell,preferred_temp(10));
      .wait(3000);
      .send(rc,untell,preferred_temp(10));
      .send(rc,tell,preferred_temp(20));
      .wait(3000);
      .send(rc,achieve,stop).

{ include("$jacamoJar/templates/common-cartago.asl") }
{ include("$jacamoJar/templates/common-moise.asl") }
