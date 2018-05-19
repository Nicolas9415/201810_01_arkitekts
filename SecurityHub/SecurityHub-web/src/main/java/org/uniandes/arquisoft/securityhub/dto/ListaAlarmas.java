package org.uniandes.arquisoft.securityhub.dto;

import java.io.Serializable;
import java.util.ArrayList;
import java.util.Date;
import java.util.List;

public class ListaAlarmas implements Serializable {
	
	/**
	 * 
	 */
	private static final long serialVersionUID = -3952287188866732430L;
	private List<AlarmaDto> alarmas;
	
	public ListaAlarmas() {
		alarmas = new ArrayList<>();
	}
	
	public void registrarAlarma(String mensajeAlarma, Date fechaAlarma) {
		AlarmaDto alarma = new AlarmaDto(mensajeAlarma, fechaAlarma);
		alarmas.add(alarma);
	}
	
	public Boolean hayAlarmas() {
		return !alarmas.isEmpty();
	}

	public List<AlarmaDto> getAlarmas() {
		return alarmas;
	}

	public void setAlarmas(List<AlarmaDto> alarmas) {
		this.alarmas = alarmas;
	}
}
