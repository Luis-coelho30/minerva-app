package br.com.puctech.minerva_student_app.repo;

import br.com.puctech.minerva_student_app.model.Nota;
import br.com.puctech.minerva_student_app.model.Usuario;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.data.jpa.repository.Modifying;
import org.springframework.data.jpa.repository.Query;
import org.springframework.stereotype.Repository;

import java.util.List;

@Repository
public interface NotaRepository extends JpaRepository<Nota, Long> {

    @Query(nativeQuery = true,
            value = "SELECT NOTA.* FROM NOTA " +
                    "INNER JOIN DISCIPLINA AS disc ON disc.ID = NOTA.DISCIPLINA_ID " +
                    "WHERE disc.ID = ?1")
    List<Nota> findNotasByDisciplina(Long id);

    void deleteAllByDisciplinaId(Long id);

    void deleteByDisciplinaUsuario(Usuario usuario);

    @Query(nativeQuery = true,
            value = "SELECT NOTA.* FROM NOTA " +
                    "INNER JOIN DISCIPLINA AS disc ON disc.ID = NOTA.DISCIPLINA_ID " +
                    "INNER JOIN USUARIO AS u ON u.ID = disc.USUARIO_ID " +
                    "WHERE u.EMAIL = ?1")
    List<Nota> findAllByUserMail(String email);
}
