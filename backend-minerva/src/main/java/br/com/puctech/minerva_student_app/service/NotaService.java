package br.com.puctech.minerva_student_app.service;

import br.com.puctech.minerva_student_app.exception.disciplina.DisciplinaNaoEncontradaException;
import br.com.puctech.minerva_student_app.exception.nota.NotaNaoEncontradaException;
import br.com.puctech.minerva_student_app.model.Disciplina;
import br.com.puctech.minerva_student_app.model.Nota;
import br.com.puctech.minerva_student_app.repo.NotaRepository;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

import java.util.List;
import java.util.Map;
import java.util.Optional;
import java.util.stream.Collectors;

@Service
public class NotaService {

    @Autowired
    private NotaRepository notaRepository;

    @Autowired
    private DisciplinaService disciplinaService;

    @Transactional(readOnly = true)
    public List<Nota> listarNotasPorDisciplina(Long id) {
        return notaRepository.findNotasByDisciplina(id);
    }

    @Transactional(readOnly = true)
    public Optional<Nota> buscarPorID(Long id) {
        return notaRepository.findById(id);
    }

    @Transactional
    public Nota salvarNota(Nota nota, Long disciplinaId) {
        Optional<Disciplina> disciplinaOpt = disciplinaService.buscarPorId(disciplinaId);

        if (disciplinaOpt.isEmpty()) {
            throw new DisciplinaNaoEncontradaException(disciplinaId);
        }

        Disciplina disciplina = disciplinaOpt.get();

        nota.setDisciplina(disciplina);
        Nota notaSalva = notaRepository.save(nota);

        recalcularMediaDisciplina(disciplina);

        return notaSalva;
    }

    @Transactional
    public Nota atualizarNota(Long id, Nota novaNota, Long disciplinaId) {
        Disciplina disciplina = disciplinaService.buscarPorId(disciplinaId)
                .orElseThrow(() -> new DisciplinaNaoEncontradaException(disciplinaId));

        Nota nota = notaRepository.findById(id)
                .orElseThrow(() -> new NotaNaoEncontradaException(id));

        nota.setDescricao(novaNota.getDescricao());
        nota.setValor(novaNota.getValor());
        nota.setPeso(novaNota.getPeso());
        nota.setDisciplina(disciplina);

        Nota notaSalva = notaRepository.save(nota);

        recalcularMediaDisciplina(disciplina);

        return notaSalva;
    }

    @Transactional
    public void deletarNota(Long id) {
        Nota nota = notaRepository.findById(id)
                .orElseThrow(() -> new NotaNaoEncontradaException(id));

        Disciplina disciplina = nota.getDisciplina();

        notaRepository.delete(nota);

        recalcularMediaDisciplina(disciplina);
    }

    @Transactional(readOnly = true)
    public Map<Long, List<Nota>> listarNotasAgrupadasPorDisciplina(String email) {
        List<Nota> todasAsNotas = notaRepository.findAllByUserMail(email);

        return todasAsNotas.stream()
                .collect(Collectors.groupingBy(nota -> nota.getDisciplina().getId()));
    }

    private void recalcularMediaDisciplina(Disciplina disciplina) {
        List<Nota> todasAsNotas = notaRepository.findNotasByDisciplina(disciplina.getId());

        double somaValoresPonderados = 0.0;
        int somaTotalPesos = 0;

        for (Nota n : todasAsNotas) {
            somaValoresPonderados += n.getValor() * n.getPeso();
            somaTotalPesos += n.getPeso();
        }

        if (somaTotalPesos > 0) {
            double novaMedia = somaValoresPonderados / somaTotalPesos;
            disciplina.setMediaAtual(novaMedia);
        } else {
            disciplina.setMediaAtual(0.0);
        }

        disciplinaService.salvarDisciplina(disciplina);
    }
}
