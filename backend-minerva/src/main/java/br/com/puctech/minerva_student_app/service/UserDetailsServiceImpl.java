package br.com.puctech.minerva_student_app.service;

import br.com.puctech.minerva_student_app.model.UserDetailsImpl;
import br.com.puctech.minerva_student_app.model.Usuario;
import br.com.puctech.minerva_student_app.repo.UserRepository;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.security.core.userdetails.UserDetails;
import org.springframework.security.core.userdetails.UserDetailsService;
import org.springframework.security.core.userdetails.UsernameNotFoundException;
import org.springframework.stereotype.Service;

@Service
public class UserDetailsServiceImpl implements UserDetailsService {

    @Autowired
    private UserRepository userRepository;

    @Override
    public UserDetails loadUserByUsername(String email) throws UsernameNotFoundException {

        Usuario usuario = userRepository.findByEmail(email);

        if(usuario == null) {
            throw new UsernameNotFoundException("User not found");
        }

        return new UserDetailsImpl(usuario);
    }
}
