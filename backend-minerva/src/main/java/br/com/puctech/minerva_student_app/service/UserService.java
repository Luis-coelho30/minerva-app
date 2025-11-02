package br.com.puctech.minerva_student_app.service;

import br.com.puctech.minerva_student_app.exception.user.AuthenticationFailedException;
import br.com.puctech.minerva_student_app.exception.user.CredenciaisIncorretasException;
import br.com.puctech.minerva_student_app.exception.user.EmailJaCadastradoException;

import br.com.puctech.minerva_student_app.exception.user.UsuarioNaoEncontradoException;
import br.com.puctech.minerva_student_app.model.Usuario;
import br.com.puctech.minerva_student_app.repo.*;
import org.springframework.beans.factory.annotation.Autowired;

import org.springframework.security.authentication.AuthenticationManager;
import org.springframework.security.authentication.UsernamePasswordAuthenticationToken;
import org.springframework.security.core.Authentication;
import org.springframework.security.core.AuthenticationException;
import org.springframework.security.core.userdetails.UsernameNotFoundException;
import org.springframework.security.crypto.bcrypt.BCryptPasswordEncoder;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

@Service
public class UserService {

    @Autowired
    private UserRepository userRepository;
    @Autowired
    private TarefaRepository tarefaRepository;
    @Autowired
    private DisciplinaRepository disciplinaRepository;
    @Autowired
    private ArquivoRepository arquivoRepository;
    @Autowired
    private NotaRepository notaRepository;

    @Autowired
    private AuthenticationManager authenticationManager;

    @Autowired
    private JWTService jwtService;

    private final BCryptPasswordEncoder encoder = new BCryptPasswordEncoder(12);

    @Transactional(readOnly = true)
    public Usuario getUsuario(String email) {
        Usuario usuario = userRepository.findByEmail(email);
        if(usuario==null) {
            throw new UsernameNotFoundException("Usuário não foi encontrado");
        }

        return usuario;
    }

    public String verificarLogin(Usuario usuario) {
        try {
            Authentication authentication = authenticationManager.authenticate(
                    new UsernamePasswordAuthenticationToken(usuario.getEmail(), usuario.getSenha())
            );

            if(authentication.isAuthenticated()) {
                return jwtService.generateToken(usuario.getEmail());
            }

            throw new AuthenticationFailedException("Falha ao autenticar usuário");
        } catch (AuthenticationException e) {
            throw new CredenciaisIncorretasException("Email ou senha inválidos");
        }
    }

    @Transactional
    public Usuario registrar(Usuario usuario) {
        if(userRepository.existsByEmail(usuario.getEmail())) {
            throw new EmailJaCadastradoException("Usuário já foi cadastrado.");
        }
        usuario.setSenha(encoder.encode(usuario.getSenha()));

        return userRepository.save(usuario);
    }

    @Transactional
    public String atualizarUsuario(String email, Usuario novoUsuario) {
        Usuario usuario = userRepository.findByEmail(email);
        if(usuario == null) {
            throw new UsernameNotFoundException("Usuário não foi encontrado.");
        } else {
            usuario.setUsername(novoUsuario.getUsername());
            usuario.setEmail(novoUsuario.getEmail());
            usuario.setSenha(encoder.encode(novoUsuario.getSenha()));
            userRepository.save(usuario);
        }

        return jwtService.generateToken(usuario.getEmail());
    }

    @Transactional
    public void deletarUsuario(String email) {

        Usuario usuario = userRepository.findByEmail(email);

        if(usuario == null) {
            throw new UsuarioNaoEncontradoException(email);
        }

        tarefaRepository.deleteByUsuario(usuario);
        arquivoRepository.deleteByUsuario(usuario);
        notaRepository.deleteByDisciplinaUsuario(usuario);
        disciplinaRepository.deleteByUsuario(usuario);

        userRepository.deleteByEmail(email);
    }
}
