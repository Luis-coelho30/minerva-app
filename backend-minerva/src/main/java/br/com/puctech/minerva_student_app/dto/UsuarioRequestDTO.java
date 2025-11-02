package br.com.puctech.minerva_student_app.dto;

import br.com.puctech.minerva_student_app.model.Usuario;
import lombok.Getter;
import lombok.NoArgsConstructor;
import lombok.Setter;
import org.springframework.beans.BeanUtils;

@Getter
@Setter
@NoArgsConstructor
public class UsuarioRequestDTO {

    private Long id;
    private String username;
    private String email;
    private String senha;

    public UsuarioRequestDTO(Usuario usuario) {
        BeanUtils.copyProperties(usuario, this);
    }
}
