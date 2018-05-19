package org.uniandes.arquisoft.securityhub.controller;

import java.io.IOException;
import java.io.Serializable;
import java.util.ArrayList;
import java.util.Date;
import java.util.List;

import javax.annotation.PostConstruct;
import javax.enterprise.context.SessionScoped;
import javax.faces.context.ExternalContext;
import javax.faces.context.FacesContext;
import javax.faces.context.Flash;
import javax.inject.Named;

import org.eclipse.paho.client.mqttv3.IMqttDeliveryToken;
import org.eclipse.paho.client.mqttv3.MqttCallback;
import org.eclipse.paho.client.mqttv3.MqttClient;
import org.eclipse.paho.client.mqttv3.MqttConnectOptions;
import org.eclipse.paho.client.mqttv3.MqttException;
import org.eclipse.paho.client.mqttv3.MqttMessage;
import org.omnifaces.util.Ajax;
import org.uniandes.arquisoft.securityhub.dto.ResidenciaDto;

@SessionScoped
@Named("residenciasController")
public class BandejaResidenciasController implements Serializable, MqttCallback {
	
	/**
	 * 
	 */
	private static final long serialVersionUID = -7827306814425529631L;
	
	private List<ResidenciaDto> residencias;
	
	private MqttClient myClient;
	private MqttConnectOptions connOpt;

	private static final String BROKER_URL = "tcp://192.168.43.148:1883";
	private static final String BASE_TOPIC = "security/isis2503/#";
	private static final String ARTIFACT_ID = "securityHub";
	
	private Boolean updateRequired;
	

	@PostConstruct
	public void init() {
		residencias = new ArrayList<>();
		for(int i = 1; i < 10; i++) {
			ResidenciaDto r = new ResidenciaDto(i, "Propietario" + i, 1, "A", String.valueOf(i*100));
			residencias.add(r);
		}
		for(int i = 10; i < 20; i++) {
			ResidenciaDto r = new ResidenciaDto(i, "Propietario" + i, 2, "A", String.valueOf(i*100));
			residencias.add(r);
		}
		for(int i = 20; i < 30; i++) {
			ResidenciaDto r = new ResidenciaDto(i, "Propietario" + i, 3, "A", String.valueOf(i*100));
			residencias.add(r);
		}
		
		String clientID = ARTIFACT_ID;
		connOpt = new MqttConnectOptions();

		connOpt.setCleanSession(true);
		connOpt.setKeepAliveInterval(30);

		// Connect to Broker
		try {
			myClient = new MqttClient(BROKER_URL, clientID);
			myClient.setCallback(this);
			myClient.connect(connOpt);
		} catch (MqttException e) {
			e.printStackTrace();
		}

		System.out.println("Connected to " + BROKER_URL);

		String myTopic = BASE_TOPIC;
		setUpdateRequired(Boolean.FALSE);

		// subscribe to topic if subscriber
		try {
			int subQoS = 0;
			myClient.subscribe(myTopic, subQoS);
		} catch (Exception e) {
			e.printStackTrace();
		}
		
		checkAndUpdate();
	}

	public List<ResidenciaDto> getResidencias() {
		return residencias;
	}

	public void setResidencias(List<ResidenciaDto> residencias) {
		this.residencias = residencias;
	}
	
	public void checkAndUpdate() {
		if(getUpdateRequired()) {
			Ajax.update("dtResidencias");
		}
	}

	@Override
	public void connectionLost(Throwable cause) {
		// TODO Auto-generated method stub
		
	}

	@Override
	public void messageArrived(String topic, MqttMessage message) throws Exception {
		String messageString = new String(message.getPayload());
		System.out.println("-------------------------------------------------");
		System.out.println("| Topic:" + topic);
		System.out.println("| Message: " + messageString);
		System.out.println("-------------------------------------------------");
		
		getResidencias().get(0).getAlarmas().registrarAlarma(messageString, new Date());
		setUpdateRequired(Boolean.TRUE);
	}

	@Override
	public void deliveryComplete(IMqttDeliveryToken token) {
		// TODO Auto-generated method stub
		
	}

	public Boolean getUpdateRequired() {
		return updateRequired;
	}

	public void setUpdateRequired(Boolean updateRequired) {
		this.updateRequired = updateRequired;
	}
	
	public void mostrarAlarmasResidencia(ResidenciaDto residencia) {
		Flash flash = FacesContext.getCurrentInstance().getExternalContext().getFlash();
		flash.put("residencia", residencia);
		ExternalContext externalContext = FacesContext.getCurrentInstance().getExternalContext();
		try {
			externalContext.redirect("bandejaAlarmas.xhtml");
		} catch (IOException e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
		}
	}
}
