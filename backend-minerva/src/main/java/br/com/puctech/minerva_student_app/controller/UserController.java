package br.com.puctech.minerva_student_app.controller;

import br.com.puctech.minerva_student_app.dto.TokenResponseDTO;
import br.com.puctech.minerva_student_app.dto.UsuarioRequestDTO;
import br.com.puctech.minerva_student_app.dto.UsuarioResponseDTO;
import br.com.puctech.minerva_student_app.model.Usuario;
import br.com.puctech.minerva_student_app.service.UserService;

import jakarta.servlet.http.HttpServletResponse;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.http.HttpHeaders;
import org.springframework.http.ResponseCookie;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.security.core.Authentication;
import org.springframework.web.bind.annotation.*;

import java.time.Duration;

@RestController
@RequestMapping("/usuarios")
public class UserController {

    @Autowired
    private UserService userService;

    @Value("${minerva.cookie.secure}")
    private boolean cookieSecure;

    @PostMapping("/login")
    public ResponseEntity<TokenResponseDTO> login(@RequestBody UsuarioRequestDTO usuarioRequestDTO,
                                                  HttpServletResponse response) {

        Usuario usuario = new Usuario(
                usuarioRequestDTO.getUsername(),
                usuarioRequestDTO.getEmail(),
                usuarioRequestDTO.getSenha()
        );

        String jwt = userService.verificarLogin(usuario);

        if (jwt.isEmpty()) {
            return ResponseEntity.status(HttpStatus.UNAUTHORIZED).body(null);
        }

        ResponseCookie cookie = ResponseCookie.from("jwt", jwt)
                .httpOnly(true)
                .secure(cookieSecure)
                .path("/")
                .sameSite("None")
                .maxAge(Duration.ofHours(1))
                .build();

        return ResponseEntity.ok()
                .header(HttpHeaders.SET_COOKIE, cookie.toString())
                .build();
    }

    @PostMapping("/register")
    public ResponseEntity<UsuarioResponseDTO> register(@RequestBody UsuarioRequestDTO usuarioRequestDTO) {
        Usuario usuario = new Usuario(usuarioRequestDTO.getUsername(), usuarioRequestDTO.getEmail(), usuarioRequestDTO.getSenha());
        Usuario salvo = userService.registrar(usuario);
        UsuarioResponseDTO responseDTO = new UsuarioResponseDTO(salvo);

        return ResponseEntity.status(HttpStatus.CREATED).body(responseDTO);
    }

    @PutMapping("/me")
    public ResponseEntity<String> atualizarUsuario(Authentication authentication, @RequestBody UsuarioRequestDTO usuarioDTO) {
        Usuario novoUsuario = new Usuario(usuarioDTO.getUsername(), usuarioDTO.getEmail(), usuarioDTO.getSenha());

        String jwt = userService.atualizarUsuario(authentication.getName(), novoUsuario);

        if (jwt.isEmpty()) {
            return ResponseEntity.status(HttpStatus.UNAUTHORIZED).body(null);
        }

        ResponseCookie cookie = ResponseCookie.from("jwt", jwt)
                .httpOnly(true)
                .secure(cookieSecure)
                .path("/")
                .sameSite("None")
                .maxAge(Duration.ofHours(1))
                .build();

        return ResponseEntity.ok()
                .header(HttpHeaders.SET_COOKIE, cookie.toString())
                .build();
    }

    @DeleteMapping("/me")
    public ResponseEntity<Void> deletarUsuario(Authentication authentication) {
        userService.deletarUsuario(authentication.getName());
        return ResponseEntity.noContent().build();
    }
}
