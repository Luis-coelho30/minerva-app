package br.com.puctech.minerva_student_app.service;

import br.com.puctech.minerva_student_app.exception.disciplina.DisciplinaNaoEncontradaException;
import br.com.puctech.minerva_student_app.model.Disciplina;
import br.com.puctech.minerva_student_app.model.Tarefa;
import br.com.puctech.minerva_student_app.repo.TarefaRepository;
import org.springframework.transaction.annotation.Transactional;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

import java.util.List;
import java.util.Optional;

@Service
public class TarefaService {

    @Autowired
    private TarefaRepository tarefaRepository;

    @Autowired
    private DisciplinaService disciplinaService;

    @Transactional(readOnly = true)
    public List<Tarefa> listarTarefasPorUsuario(String email) {
        return tarefaRepository.findTaskByUsermail(email);
    }

    @Transactional(readOnly = true)
    public List<Tarefa> buscarPorDisciplina(String email, Long disciplinaId) {
        return tarefaRepository.findTaskByDisciplina(email, disciplinaId);
    }

    @Transactional
    public Tarefa salvarTarefa(Tarefa tarefa) {
        return tarefaRepository.save(tarefa);
    }

    @Transactional
    public Tarefa salvarTarefa(Tarefa tarefa, Long disciplinaId) {

        Optional<Disciplina> disciplina = disciplinaService.buscarPorId(disciplinaId);

        if(disciplina.isEmpty()) {
            throw new DisciplinaNaoEncontradaException(disciplinaId);
        }

        tarefa.setDisciplina(disciplina.get());

        return tarefaRepository.save(tarefa);
    }

    @Transactional
    public Tarefa atualizarTarefa(Long id, Tarefa novaTarefa) {
        return tarefaRepository.findById(id)
                .map( tarefa -> {
                    tarefa.setTitulo(novaTarefa.getTitulo());
                    tarefa.setDescricao(novaTarefa.getDescricao());
                    tarefa.setStatus(novaTarefa.getStatus());
                    tarefa.setDisciplina(null);
                    tarefa.setPrioridade(novaTarefa.getPrioridade());
                    tarefa.setArquivada((novaTarefa.getArquivada()));
                    tarefa.setDataInicio(novaTarefa.getDataInicio());
                    tarefa.setDataFinal(novaTarefa.getDataFinal());
                    tarefa.setConcluido_em(novaTarefa.getConcluido_em());

                    return tarefaRepository.save(tarefa);
                })
                .orElseGet(() -> tarefaRepository.save(novaTarefa));
    }

    @Transactional
    public Tarefa atualizarTarefa(Long id, Tarefa tarefa, Long disciplinaId) {

        Optional<Disciplina> disciplina = disciplinaService.buscarPorId(disciplinaId);

        if(disciplina.isEmpty()) {
            throw new DisciplinaNaoEncontradaException(disciplinaId);
        }

        return tarefaRepository.findById(id)
                .map( tarefaN -> {
                    tarefa.setTitulo(tarefa.getTitulo());
                    tarefa.setDescricao(tarefa.getDescricao());
                    tarefa.setStatus(tarefa.getStatus());
                    tarefa.setPrioridade(tarefa.getPrioridade());
                    tarefa.setArquivada((tarefa.getArquivada()));
                    tarefa.setDisciplina(disciplina.get());
                    tarefa.setDataInicio(tarefa.getDataInicio());
                    tarefa.setDataFinal(tarefa.getDataFinal());
                    tarefa.setConcluido_em(tarefa.getConcluido_em());

                    return tarefaRepository.save(tarefa);
                })
                .orElseGet(() -> tarefaRepository.save(tarefa));
    }

    @Transactional
    public void deletarTarefa(Long id) {
        tarefaRepository.deleteById(id);
    }
}
