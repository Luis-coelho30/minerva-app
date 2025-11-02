package br.com.puctech.minerva_student_app.repo;

import br.com.puctech.minerva_student_app.model.Usuario;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.data.jpa.repository.Query;
import org.springframework.stereotype.Repository;

@Repository
public interface UserRepository extends JpaRepository<Usuario, Long> {

    Usuario findByUsername(String username);
    boolean existsByEmail(String email);
    Usuario findByEmail(String email);

    void deleteByEmail(String email);
}
