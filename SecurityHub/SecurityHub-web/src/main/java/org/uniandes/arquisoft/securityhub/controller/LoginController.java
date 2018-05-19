package org.uniandes.arquisoft.securityhub.controller;

import java.io.IOException;
import java.io.Serializable;
import java.util.Map;
import java.util.concurrent.ConcurrentHashMap;

import javax.annotation.PostConstruct;
import javax.faces.context.ExternalContext;
import javax.faces.context.FacesContext;
import javax.inject.Named;

import org.omnifaces.cdi.ViewScoped;

@ViewScoped
@Named("loginController")
public class LoginController implements Serializable {

	/**
	 * 
	 */
	private static final long serialVersionUID = -1071933826912446270L;
	
	private Map<String, String> usuarios;
	private String userIn;
	private String pwdIn;
	
	@PostConstruct
	public void init() {
		usuarios = new ConcurrentHashMap<>();
		usuarios.put("camilo@securityHub.co", "1234");
		usuarios.put("nicolas@securityHub.co", "1234");
		usuarios.put("adminYale@securityHub.co", "1234");
		usuarios.put("adminSecurity@securityHub.co", "1234");
	}
	
	
	public void autenticar() {
		String passV = usuarios.get(userIn);
		if(passV!= null && passV.equals(pwdIn)) {
			ExternalContext externalContext = FacesContext.getCurrentInstance().getExternalContext();
			try {
				externalContext.redirect("bandejaResidencias.xhtml");
			} catch (IOException e) {
				// TODO Auto-generated catch block
				e.printStackTrace();
			}
		}
	}


	public String getUserIn() {
		return userIn;
	}


	public void setUserIn(String userIn) {
		this.userIn = userIn;
	}


	public String getPwdIn() {
		return pwdIn;
	}


	public void setPwdIn(String pwdIn) {
		this.pwdIn = pwdIn;
	}
	
	public void logout() {
		ExternalContext externalContext = FacesContext.getCurrentInstance().getExternalContext();
		try {
			externalContext.redirect("index.xhtml");
		} catch (IOException e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
		}
	}
	
	

}
