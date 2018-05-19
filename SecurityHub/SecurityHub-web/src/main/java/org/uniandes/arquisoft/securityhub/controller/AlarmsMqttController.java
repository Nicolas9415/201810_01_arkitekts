package org.uniandes.arquisoft.securityhub.controller;

import java.io.Serializable;
import java.util.Date;

import javax.annotation.PostConstruct;
import javax.inject.Inject;

import org.eclipse.paho.client.mqttv3.IMqttDeliveryToken;
import org.eclipse.paho.client.mqttv3.MqttCallback;
import org.eclipse.paho.client.mqttv3.MqttClient;
import org.eclipse.paho.client.mqttv3.MqttConnectOptions;
import org.eclipse.paho.client.mqttv3.MqttException;
import org.eclipse.paho.client.mqttv3.MqttMessage;

public class AlarmsMqttController implements Serializable, MqttCallback {

	/**
	 * 
	 */
	private static final long serialVersionUID = 6591152455807441195L;
	
	@Inject
	private BandejaResidenciasController residenciasController;
	
	MqttClient myClient;
	MqttConnectOptions connOpt;

	private static final String BROKER_URL = "tcp://192.168.43.148:1883";
	private static final String BASE_TOPIC = "security/isis2503/#";
	private static final String ARTIFACT_ID = "securityHub";
	
	private Boolean updateRequired;
	
	/**
	 * 
	 * runClient
	 * The main functionality of this simple example.
	 * Create a MQTT client, connect to broker, pub/sub, disconnect.
	 * 
	 */
	@PostConstruct
	public void init() {
		// setup MQTT Client
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
	}

	

	/**
	 * 
	 * connectionLost
	 * This callback is invoked upon losing the MQTT connection.
	 * 
	 */
	@Override
	public void connectionLost(Throwable t) {
//		System.out.println("Connection lost!");
		init();
	}

	/**
	 * 
	 * deliveryComplete
	 * This callback is invoked when a message published by this client
	 * is successfully received by the broker.
	 * 
	 */
	@Override
	public void deliveryComplete(IMqttDeliveryToken token) {
		//System.out.println("Pub complete" + new String(token.getMessage().getPayload()));
	}

	/**
	 * 
	 * messageArrived
	 * This callback is invoked when a message is received on a subscribed topic.
	 * 
	 */
	@Override
	public void messageArrived(String topic, MqttMessage message) throws Exception {
		String messageString = new String(message.getPayload());
		System.out.println("-------------------------------------------------");
		System.out.println("| Topic:" + topic);
		System.out.println("| Message: " + messageString);
		System.out.println("-------------------------------------------------");
		
		residenciasController.getResidencias().get(0).getAlarmas().registrarAlarma(messageString, new Date());
		setUpdateRequired(Boolean.TRUE);
	}

	public Boolean getUpdateRequired() {
		return updateRequired;
	}

	public void setUpdateRequired(Boolean updateRequired) {
		this.updateRequired = updateRequired;
	}

}
