package org.uniandes.arquisoft.securityhub.dto;

import java.io.Serializable;

public class ResidenciaDto implements Serializable {
	
	/**
	 * 
	 */
	private static final long serialVersionUID = 2162791509224036369L;
	private Integer id;
	private String propietario;
	private Integer piso;
	private String torre;
	private String numeroApto;
	private ListaAlarmas alarmas;
	
	public Integer getId() {
		return id;
	}

	public void setId(Integer id) {
		this.id = id;
	}

	public ResidenciaDto(Integer id, String propietario, Integer piso, String torre, String numeroApto) {
		this.id = id;
		this.propietario = propietario;
		this.piso = piso;
		this.torre = torre;
		this.numeroApto = numeroApto;
		alarmas = new ListaAlarmas();
	}
	
	public String getPropietario() {
		return propietario;
	}
	public void setPropietario(String propietario) {
		this.propietario = propietario;
	}
	public Integer getPiso() {
		return piso;
	}
	public void setPiso(Integer piso) {
		this.piso = piso;
	}
	public String getTorre() {
		return torre;
	}
	public void setTorre(String torre) {
		this.torre = torre;
	}
	public String getNumeroApto() {
		return numeroApto;
	}
	public void setNumeroApto(String numeroApto) {
		this.numeroApto = numeroApto;
	}

	public ListaAlarmas getAlarmas() {
		return alarmas;
	}

	public void setAlarmas(ListaAlarmas alarmas) {
		this.alarmas = alarmas;
	}

}
