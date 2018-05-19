package org.uniandes.arquisoft.securityhub.dto;

import java.io.Serializable;
import java.util.Date;

public class AlarmaDto implements Serializable {
	
	/**
	 * 
	 */
	private static final long serialVersionUID = -5866676710954262780L;
	
	private String mensajeAlarma;
	private Date fechaAlarma;
	
	public AlarmaDto(String mensajeAlarma, Date fechaAlarma) {
		this.mensajeAlarma = mensajeAlarma;
		this.fechaAlarma = fechaAlarma;
	}
	
	public String getMensajeAlarma() {
		return mensajeAlarma;
	}
	public void setMensajeAlarma(String mensajeAlarma) {
		this.mensajeAlarma = mensajeAlarma;
	}
	public Date getFechaAlarma() {
		return fechaAlarma;
	}
	public void setFechaAlarma(Date fechaAlarma) {
		this.fechaAlarma = fechaAlarma;
	}

}
