package devices;

import cartago.*;

public class HVAC extends Artifact {

	private TemperatureSensorPanel sensorPanel;
	private int temperature;

	void init(int temp){
		this.temperature = temp; // initial simulated value
		defineObsProperty("state","off");
		defineObsProperty("temperature",temperature);

		sensorPanel = new TemperatureSensorPanel(this,temp);
		sensorPanel.setVisible(true);
	}

	@OPERATION void turn_on(Object device) {
		if (getObsProperty("state").stringValue().equals("off")) {
		   getObsProperty("state").updateValue("on");
		   this.execInternalOp("updateTemperatureProc",-1);
			 System.out.println("on");
	  }
	}

	@OPERATION void turn_off(Object device) {
		if (getObsProperty("state").stringValue().equals("on")) {
   	 	 getObsProperty("state").updateValue("off");
	   	 this.execInternalOp("updateTemperatureProc",+1); // simulates that it starts heating
			 System.out.println("off");
		}
	}

	@INTERNAL_OPERATION void updateTemperatureProc(int step){
		ObsProperty prop = getObsProperty("temperature");
		while (true) {
  			this.await_time(300);
  			int temp = prop.intValue();
  			if (step < 0 && (temp <  1 || getObsProperty("state").stringValue().equals("off")))
	  			 break;
  			if (step > 0 && (temp > 40 || getObsProperty("state").stringValue().equals("on")))
	 	  		 break;
				prop.updateValue(temp+step);
				sensorPanel.setTempValue(temp+step);
	  }
	}

	void notifyNewTemperature(int value){
		getObsProperty("temperature").updateValue(value);
	}

	void notifyNewPreferredTemperature(int value){
		getObsProperty("preferred_temperature").updateValue(value);
	}

}
