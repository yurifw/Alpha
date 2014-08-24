/*
 * To change this license header, choose License Headers in Project Properties.
 * To change this template file, choose Tools | Templates
 * and open the template in the editor.
 */
package br.eb.ime.alpha.view;

import br.eb.ime.alpha.conversion.ByteConversion;
import br.eb.ime.alpha.core.Alpha;
import java.awt.Dimension;
import java.awt.GridLayout;
import java.awt.event.ActionEvent;
import java.awt.event.ActionListener;
import javax.swing.BoxLayout;
import javax.swing.JButton;
import javax.swing.JFrame;
import javax.swing.JLabel;
import javax.swing.JOptionPane;
import javax.swing.JPanel;
import javax.swing.JScrollPane;
import javax.swing.JTextArea;
import javax.swing.JTextField;
import javax.swing.border.TitledBorder;

/**
 *
 * @author yurifw
 */
public class AlphaView extends JFrame {

    private JTextField txtChave = new JTextField();

    private JTextArea txtTextoClaro = new JTextArea();
    private JTextArea txtCriptograma = new JTextArea();
    private JButton btnCriptografar = new JButton("Criptografar");

    private JTextArea txtTextoClaroBinario = new JTextArea();
    private JTextArea txtCriptogramaBinario = new JTextArea();
    private JButton btnDescriptografar = new JButton("Descriptografar");
    
    private JButton btnUtilizacao = new JButton("Utilização");

    public AlphaView() {
        int max = Integer.MAX_VALUE;
        String instrucoes = "<html>Especificações:<br><br>Tamanho do bloco: 128 bites<br>Número de Iterações: 16<br>Tamanho da chave utilizada: 128 bites</html>";
        

        this.setSize(600, 600);
        this.setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
        this.setTitle("Alpha");

        JPanel container = new JPanel();
        BoxLayout layout = new BoxLayout(container, BoxLayout.Y_AXIS);
        container.setLayout(layout);

        JPanel panelInstrucao = new JPanel(new GridLayout(1, 1));
        panelInstrucao.add(new JLabel(instrucoes));
        panelInstrucao.setMaximumSize(new Dimension(max, 200));
        container.add(panelInstrucao);
        
        JPanel panelUtilizacao = new JPanel(new GridLayout(1, 1));
        panelUtilizacao.add(btnUtilizacao);
        panelUtilizacao.setMaximumSize(new Dimension(200, 40));
        container.add(panelUtilizacao);
        
        JPanel panelChave = new JPanel(new GridLayout(2, 1));
        panelChave.add(new JLabel("Chave"));
        panelChave.add(txtChave);
        panelChave.setMaximumSize(new Dimension(max, 60));
        container.add(panelChave);

        JPanel panelTextoClaro = new JPanel(new GridLayout(1, 2));
        JScrollPane scrollTxtClaro = new JScrollPane(txtTextoClaro);
        scrollTxtClaro.setBorder(new TitledBorder("Texto Claro"));
        JScrollPane scrollTxtClaroBinario = new JScrollPane(txtTextoClaroBinario);
        scrollTxtClaroBinario.setBorder(new TitledBorder("Texto Claro (em binário)"));
        panelTextoClaro.add(scrollTxtClaro);
        panelTextoClaro.add(scrollTxtClaroBinario);
        container.add(panelTextoClaro);

        JPanel panelBtnCriptografar = new JPanel(new GridLayout(1, 1));
        panelBtnCriptografar.add(btnCriptografar);
        panelBtnCriptografar.setMaximumSize(new Dimension(max, 40));
        container.add(panelBtnCriptografar);

        JPanel panelCriptograma = new JPanel(new GridLayout(1, 2));
        JScrollPane scrollCriptograma = new JScrollPane(txtCriptograma);
        JScrollPane scrollCriptogramaBinario = new JScrollPane(txtCriptogramaBinario);
        scrollCriptograma.setBorder(new TitledBorder("Criptograma"));
        scrollCriptogramaBinario.setBorder(new TitledBorder("Criptograma (em binário)"));
        panelCriptograma.add(scrollCriptograma);
        panelCriptograma.add(scrollCriptogramaBinario);
        container.add(panelCriptograma);

        JPanel panelBtnDescriptografar = new JPanel(new GridLayout(1, 1));
        panelBtnDescriptografar.add(btnDescriptografar);
        panelBtnDescriptografar.setMaximumSize(new Dimension(max, 40));
        container.add(panelBtnDescriptografar);
        

        configuraTextArea();
        addListeners();

        this.add(container);
        
    }

    private void configuraTextArea() {
        txtCriptograma.setWrapStyleWord(true);
        txtCriptograma.setLineWrap(true);
        txtCriptogramaBinario.setWrapStyleWord(true);
        txtCriptogramaBinario.setLineWrap(true);
        txtTextoClaro.setWrapStyleWord(true);
        txtTextoClaro.setLineWrap(true);
        txtTextoClaroBinario.setWrapStyleWord(true);
        txtTextoClaroBinario.setLineWrap(true);
    }

    private void addListeners() {
        btnCriptografar.addActionListener(new ActionListener() {
            @Override
            public void actionPerformed(ActionEvent e) {
                if (txtChave.getText().replaceAll(" ", "").length()!=128){
                    JOptionPane.showMessageDialog(rootPane, "A chave deve conter 128 bites","Erro",JOptionPane.ERROR_MESSAGE);
                    return;
                }
                int msg[];
                if (txtTextoClaro.getText().replaceAll(" ", "").isEmpty()){
                    msg = ByteConversion.binaryStringToInt(txtTextoClaroBinario.getText());
                } else {
                    msg = ByteConversion.stringToInt(txtTextoClaro.getText());
                }
                
                int key[] = ByteConversion.binaryStringToInt(txtChave.getText());
                int criptograma[] = Alpha.alpha(msg, key, 1, 16);
                
                txtTextoClaroBinario.setText(Alpha.printB(msg)); 
                txtCriptograma.setText(ByteConversion.intToString(criptograma));
                txtCriptogramaBinario.setText(Alpha.printB(criptograma));
                txtTextoClaro.setText(ByteConversion.intToString(ByteConversion.binaryStringToInt(txtTextoClaroBinario.getText())));
                
            }
        });

        btnDescriptografar.addActionListener(new ActionListener() {
            @Override
            public void actionPerformed(ActionEvent e) {
                if (txtChave.getText().replaceAll(" ", "").length()!=128){
                    JOptionPane.showMessageDialog(rootPane, "A chave deve conter 128 bites","Erro",JOptionPane.ERROR_MESSAGE);
                    return;
                }
                int criptograma[] = ByteConversion.binaryStringToInt(txtCriptogramaBinario.getText());
                
                int key[] = ByteConversion.binaryStringToInt(txtChave.getText());
                int textoClaro[] = Alpha.alpha(criptograma, key, 0, 16);
                
                txtCriptograma.setText(ByteConversion.intToString(criptograma));
                txtTextoClaro.setText(ByteConversion.intToString(textoClaro));
                txtTextoClaroBinario.setText(Alpha.printB(textoClaro));
                

            }
        });
        
        btnUtilizacao.addActionListener(new ActionListener() {
            @Override
            public void actionPerformed(ActionEvent e) {
                String utilizacao = "<html>Utilização:<br>Digite a chave em caracteres binários no campo correspondente,<br>"
                        + " cada grupo de 8 bites deve ser separado por um espaço em branco.<br>";
                utilizacao += "Ao clicar no botão \"Criptografar\", o texto em claro (se tanto o binario quanto o ASCII estiverem<br>"
                        + " preenchidos, o ASCII será considerado) será convertido para binario e apresentado no devido campo,<br>"
                + " então será cifrado e apresentado em binario e em ASCII, cada um em seu respectivo campo.<br>"
                        + " Para descriptografar, utilize apenas a entrada de dados binários, o texto em ASCII não é confiável<br>"
                        + " devido a codificação dos caracteres."
                + "<br>Obs.: o criptograma provavelmente conterá caracteres não imprimíveis em ASCII.</html>";
                JOptionPane.showMessageDialog(rootPane, utilizacao, "Ajuda", JOptionPane.INFORMATION_MESSAGE);
            }
        });

    }
}
