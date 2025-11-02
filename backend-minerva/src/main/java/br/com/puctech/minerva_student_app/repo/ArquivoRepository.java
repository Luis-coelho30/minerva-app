package br.com.puctech.minerva_student_app.repo;

import br.com.puctech.minerva_student_app.model.Arquivo;
import br.com.puctech.minerva_student_app.model.Usuario;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.data.jpa.repository.Query;
import org.springframework.stereotype.Repository;

import java.util.List;

@Repository
public interface ArquivoRepository extends JpaRepository<Arquivo, Long> {

    @Query(nativeQuery = true,
            value = "SELECT ARQUIVO.* FROM ARQUIVO " +
                    "INNER JOIN USUARIO AS u ON u.ID = ARQUIVO.USUARIO_ID " +
                    "WHERE u.email = ?1")
    List<Arquivo> findArquivosByUsermail(String email);

    @Query(nativeQuery = true,
            value = "SELECT ARQUIVO.* FROM ARQUIVO " +
                    "INNER JOIN DISCIPLINA AS disc ON disc.ID = ARQUIVO.DISCIPLINA_ID " +
                    "WHERE disc.id = ?1")
    List<Arquivo> findArquivosByDisciplina(Long disciplinaId);

    void deleteByUsuario(Usuario usuario);
}
