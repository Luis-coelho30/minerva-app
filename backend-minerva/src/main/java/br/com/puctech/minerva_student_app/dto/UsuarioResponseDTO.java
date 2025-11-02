package br.com.puctech.minerva_student_app.dto;

import br.com.puctech.minerva_student_app.model.Usuario;
import lombok.Getter;
import lombok.Setter;
import org.springframework.beans.BeanUtils;

@Getter
@Setter
public class UsuarioResponseDTO {

    private Long id;
    private String username;
    private String email;
    private Integer xp;
    private Integer pontuacao;

    public UsuarioResponseDTO(Usuario usuario) {
        BeanUtils.copyProperties(usuario, this);
    }
}
