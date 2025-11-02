package br.com.puctech.minerva_student_app.service;

import br.com.puctech.minerva_student_app.model.Arquivo;
import br.com.puctech.minerva_student_app.model.Disciplina;
import br.com.puctech.minerva_student_app.repo.ArquivoRepository;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

import java.util.List;
import java.util.Optional;

@Service
public class ArquivoService {

    @Autowired
    private ArquivoRepository arquivoRepository;

    @Autowired
    private DisciplinaService disciplinaService;

    @Transactional(readOnly = true)
    public List<Arquivo> listarArquivos(String email) {
        return arquivoRepository.findArquivosByUsermail(email);
    }

    @Transactional(readOnly = true)
    public List<Arquivo> listarArquivosPorDisciplina(Long disciplinaId) {
        return arquivoRepository.findArquivosByDisciplina(disciplinaId);
    }

    @Transactional
    public Arquivo salvarArquivo(Arquivo arquivo) {
        return arquivoRepository.save(arquivo);
    }

    @Transactional
    public Arquivo salvarArquivo(Arquivo arquivo, Long disciplinaId) {
        Optional<Disciplina> disciplina = disciplinaService.buscarPorId(disciplinaId);

        disciplina.ifPresent(arquivo::setDisciplina);

        return arquivoRepository.save(arquivo);
    }

    @Transactional
    public Arquivo atualizarArquivo(Long id, Arquivo novoArquivo) {
        return arquivoRepository.findById(id)
                .map( arquivo -> {
                    arquivo.setNomeOriginal(novoArquivo.getNomeOriginal());
                    arquivo.setUrl(novoArquivo.getUrl());
                    arquivo.setTipo(novoArquivo.getTipo());

                    return arquivoRepository.save(arquivo);
                })
                .orElseGet(() -> arquivoRepository.save(novoArquivo));
    }

    @Transactional
    public Arquivo atualizarArquivo(Long id, Arquivo novoArquivo, Long disciplinaId) {
        Optional<Disciplina> disciplina = disciplinaService.buscarPorId(disciplinaId);
        disciplina.ifPresent(novoArquivo::setDisciplina);

        return arquivoRepository.findById(id)
                .map( arquivo -> {
                    arquivo.setNomeOriginal(novoArquivo.getNomeOriginal());
                    arquivo.setUrl(novoArquivo.getUrl());
                    arquivo.setTipo(novoArquivo.getTipo());
                    arquivo.setDisciplina(novoArquivo.getDisciplina());

                    return arquivoRepository.save(arquivo);
                })
                .orElseGet(() -> arquivoRepository.save(novoArquivo));
    }

    @Transactional
    public void deletarArquivo(Long id) {
        arquivoRepository.deleteById(id);
    }
}
