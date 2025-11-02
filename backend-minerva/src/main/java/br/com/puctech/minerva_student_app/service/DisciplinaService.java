package br.com.puctech.minerva_student_app.service;

import br.com.puctech.minerva_student_app.exception.disciplina.DisciplinaNaoEncontradaException;
import br.com.puctech.minerva_student_app.model.Disciplina;
import br.com.puctech.minerva_student_app.repo.DisciplinaRepository;
import br.com.puctech.minerva_student_app.repo.NotaRepository;

import br.com.puctech.minerva_student_app.repo.TarefaRepository;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

import java.util.List;
import java.util.Optional;

@Service
public class DisciplinaService {

    @Autowired
    private DisciplinaRepository disciplinaRepository;

    @Autowired
    private NotaRepository notaRepository;

    @Autowired
    private TarefaRepository tarefaRepository;

    @Transactional(readOnly = true)
    public List<Disciplina> listarDisciplinas(String email) {
        return disciplinaRepository.findDisciplinasByUsermail(email);
    }

    @Transactional(readOnly = true)
    public Optional<Disciplina> buscarPorId(Long id) {
        return disciplinaRepository.findById(id);
    }

    @Transactional
    public Disciplina salvarDisciplina(Disciplina disciplina) {
        return disciplinaRepository.save(disciplina);
    }

    @Transactional
    public Disciplina atualizarDisciplina(Long id, Disciplina novaDisciplina) {
        Optional<Disciplina> disciplinaOpt = disciplinaRepository.findById(id);
        Disciplina disciplina;

        if(disciplinaOpt.isPresent()) {
            disciplina = disciplinaOpt.get();
            disciplina.setNome(novaDisciplina.getNome());
            disciplina.setDescricao(novaDisciplina.getDescricao());
            disciplina.setArquivada(novaDisciplina.getArquivada());
            disciplina.setMediaNecessaria(novaDisciplina.getMediaNecessaria());
            disciplina.setMediaAtual(novaDisciplina.getMediaAtual());
            disciplina.setCreditos(novaDisciplina.getCreditos());
            disciplina.setCargaHorariaAula(novaDisciplina.getCargaHorariaAula());
            disciplina.setCargaHorariaTotal(novaDisciplina.getCargaHorariaTotal());
            disciplina.setFaltasRegistradas(novaDisciplina.getFaltasRegistradas());
        } else {
            throw new DisciplinaNaoEncontradaException(id);
        }

        return disciplinaRepository.save(disciplina);
    }

    @Transactional
    public void deletarDisciplina(Long id) {

        if (!disciplinaRepository.existsById(id)) {
            throw new DisciplinaNaoEncontradaException(id);
        }

        notaRepository.deleteAllByDisciplinaId(id);

        tarefaRepository.deleteAllByDisciplinaId(id);

        disciplinaRepository.deleteById(id);
    }


}