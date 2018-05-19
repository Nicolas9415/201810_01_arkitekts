package org.uniandes.arquisoft.securityhub.controller;

import java.io.Serializable;
import java.util.ArrayList;
import java.util.List;

import javax.annotation.PostConstruct;
import javax.faces.context.FacesContext;
import javax.faces.context.Flash;
import javax.inject.Inject;
import javax.inject.Named;

import org.omnifaces.cdi.ViewScoped;
import org.uniandes.arquisoft.securityhub.dto.AlarmaDto;
import org.uniandes.arquisoft.securityhub.dto.ResidenciaDto;

@ViewScoped
@Named("alarmasController")
public class BandejaAlarmasController implements Serializable{

	/**
	 * 
	 */
	private static final long serialVersionUID = -8608293815986812883L;
	
	@Inject
	private BandejaResidenciasController residenciasController;
	
	private ResidenciaDto residencia;
	
	private List<String> tiposAlarma;
	
	@PostConstruct
	public void init() {
		Flash flash = FacesContext.getCurrentInstance().getExternalContext().getFlash();
		setResidencia((ResidenciaDto) flash.get("residencia"));
		tiposAlarma = new ArrayList<>();
		tiposAlarma.add("Door opened!!");
		tiposAlarma.add("Door opened for too long!");
		tiposAlarma.add("Door closed!!");
		tiposAlarma.add("Attempt deleted");
		tiposAlarma.add("Intento de apertura sospechosa");
		tiposAlarma.add("System locked");
		tiposAlarma.add("System unlocked");
	}

	public ResidenciaDto getResidencia() {
		return residencia;
	}

	public void setResidencia(ResidenciaDto residencia) {
		this.residencia = residencia;
	}

	public void pollAlarmas() {
		for(AlarmaDto a : residenciasController.getResidencias().get(residencia.getId()-1).getAlarmas().getAlarmas()) {
			if (!residencia.getAlarmas().getAlarmas().contains(a)){
				residencia.getAlarmas().getAlarmas().add(a);
			}
		}
		
//		residencia = residenciasController.getResidencias().get();
	}

	public List<String> getTiposAlarma() {
		return tiposAlarma;
	}

	public void setTiposAlarma(List<String> tiposAlarma) {
		this.tiposAlarma = tiposAlarma;
	}

}
