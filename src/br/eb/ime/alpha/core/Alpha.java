/*
 * To change this license header, choose License Headers in Project Properties.
 * To change this template file, choose Tools | Templates
 * and open the template in the editor.
 */

package br.eb.ime.alpha.core;

import br.eb.ime.alpha.conversion.ByteConversion;

/**
 *
 * @author yurifw
 */

        /**
         * ***************** comentarios iniciais ********************************
 Este codigo foi criado para realizar um teste na versao 2 do         *
 cifrador Alpha com vetor de teste (mesmo do FIPS 197)                *
 nesta versao a transformação nAlpha usa os quatro primeiros         *
 bites do baite a esquerda para um deslocamento complementar na       *
 tabela (12x8 bits). Esta versao suporta chaves de 128 bites e        *
         * ate 17 iterações(definido por Nr)                                    *
         * A F Exp Ch é a mesma do Rijndael, com 17 valores de R Con            *
         * Para usar mais de 17 iteracoes, aumentar as R Con ou mudar a         *
         * F Exp Ch                                                             *
         * chaves independentes podem ser usadas desde que altere-se a          *
         * F Exp Ch                                                             *
         * Autor: Jorge de A. Lambert                                           *
         * Jan/04                                                               *
         * **********************************************************************/
public class Alpha {


    /*****************************************************************
     ****              metodo cifraBloco - cifra                     ******
      argumento = int[128] binario e  int[128] binario ****** 
 retorna = int [128] binario = criptograma             ******
     *****************************************************************/
    public static int[] cifraBloco(int MSG[], int KEY[], int cifra, int Nr) {
        int L_anterior[] = new int[64];
        int R_anterior[] = new int[64];
        int L[] = new int[64];
        int R[] = new int[64];
        int temp[] = new int[4];
        int  i, j;
        int cripto[] = new int[128];

        

        /********************************************************
         *          expande a chave                             *
         ********************************************************/
        int K[][] = expandeChave(KEY, Nr); // (EXPAND KEY)
        int Ke[][] = new int[Nr][64];
        int Kd[][] = new int[Nr][64];
    // aqui a chave ja expandida

        /**
         * ******************************************************
         * exibe sub-chaves *
 *******************************************************
         */
        for (i = 0; i < Nr; i++) {//para gerar ilustração das sub-chaves
            for (j = 0; j < 32; j++) {// exibe sub-chaves
                temp[0] = K[i][4 * j];
                temp[1] = K[i][(4 * j) + 1];
                temp[2] = K[i][(4 * j) + 2];
                temp[3] = K[i][(4 * j) + 3];
            }// fim do for j
        }// fim do loop de exibicao das sub-chaves

        /**********************************************************************
         *                        CIFRA ENTRADA                               *
         **********************************************************************/
        
        /*********************************************************
         *                      atribui Ke, Kd, L0 e R0          *
         *********************************************************/
        for (j = 0; j < 64; j++) {
            L_anterior[j] = MSG[j];//L zero
            R_anterior[j] = MSG[j + 64];//R zero
        }// fim do for j

        for (i = 0; i < Nr; i++) {
            if (cifra == 1) {// se vai cifrar, sub-chaves na ordem normal
                for (j = 0; j < 64; j++) {
                    Ke[i][j] = K[i][j];
                    Kd[i][j] = K[i][j + 64];
                }// fim do for j
            }//fim do if cifra=1
            if (cifra == 0) {// se vai decifrar, sub-chaves na ordem inversa
                for (j = 0; j < 64; j++) {
                    Ke[i][j] = K[Nr - 1 - i][j];
                    Kd[i][j] = K[Nr - 1 - i][j + 64];
                }// fim do for j
            }//fim do if cifra=0
        }// fim do for i
        // estao atribuidos todos os Ke e Kd, L0 e R0

        /**********************************************************
         *                 iterações                              *
         **********************************************************/
        int temporario[] = new int[64];
        for (i = 0; i < Nr; i++) {// versao com Nr iteracoes (p=0)
            // calcula L[i]=R[i-1]+Ke[i-1]
            for (j = 0; j < 64; j++) {
                L[j] = (R_anterior[j] + Ke[i][j]) % 2;
                temporario[j] = L[j];
            }



//___________________________________________________________
// atribui R(i-1) ao temporario ("estado")
            for (j = 0; j < 64; j++) {
                temporario[j] = R_anterior[j];
            }


//____________________________________________________________
            if (cifra == 0) {//soma Ke ao temporario, se decifracao
                for (j = 0; j < 64; j++) {
                    temporario[j] = (temporario[j] + Ke[i][j]) % 2;
                }



            }
//____________________________________________________________

            temporario = lAlpha(temporario);

//___________________________________________________________
            for (j = 0; j < 64; j++) {// chavei-a o vetor temporario para entrada na TNL
                temporario[j] = (temporario[j] + Kd[i][j]) % 2;
            }
           
//______________________________________________________________
            int[] baite = new int[8];
            int[] delta_linha = new int[8];
            delta_linha[0]
                    = temporario[56] * 8 + temporario[57] * 4 + temporario[58] * 2 + temporario[59];
            for (j = 0; j < 7; j++) {
                delta_linha[(j + 1)] = temporario[j * 8] * 8 + temporario[(j * 8) + 1] * 4
                        + temporario[(j * 8) + 2] * 2 + temporario[(j * 8) + 3];
            }
            for (j = 0; j < 8; j++) {
                for (int k = 0; k < 8; k++) {
                    baite[k] = temporario[8 * j + k];
                }
                baite = nAlpha(baite, delta_linha[j]);
                for (int k = 0; k < 8; k++) {
                    temporario[8 * j + k] = baite[k];
                }
            }

//____________________________________________________________________
//calcula R[i]
            for (j = 0; j < 64; j++) {
                R[j] = (L_anterior[j] + temporario[j]) % 2;
                L_anterior[j] = L[j];
                R_anterior[j] = R[j];
            }

        }// fim das iteracoes ***************************************
        for (j = 0; j < 64; j++) {//faz cripto=R|L (trocado intencionalmente)
            cripto[j] = R[j];//
            cripto[j + 64] = L[j];//
        }// fim do for j

        return cripto;
    }// ******************** fim do metodo cifraBloco****************************
    

    /**********************************************************************
     *****          metodo expansão da chave - (EXPAND KEY)           ***** 
     ********             argumento =  int[128] binario               *****
     *********  retorna = int [Nr][128] binario                       *****
     * ********************************************************************/
    public static int[][] expandeChave(int KEY[], int Nr) {//modificada para gerar ate 17 sub - chaves
        int XK[][] = new int[Nr][128];
        int temp1[] = new int[8];
        int temp2[] = new int[8];
        int temp3[] = new int[8];
        int temp4[] = new int[8];
        int temptemp[] = new int[8];
        String temp;
        int i, j, c, c2;
        int RCON[][] = {
            {0, 0, 0, 0, 0, 0, 0, 0},// este byte nao é usado (apenas para coerencia dos indices)
            {0, 0, 0, 0, 0, 0, 0, 1},// este byte e o RCon[1] pela notação do FIPS 197 (Nk = 4)
            {0, 0, 0, 0, 0, 0, 1, 0},// este byte e o RCon[2]
            {0, 0, 0, 0, 0, 1, 0, 0},// este byte e o RCon[3]
            {0, 0, 0, 0, 1, 0, 0, 0},// este byte e o RCon[4]
            {0, 0, 0, 1, 0, 0, 0, 0},// este byte e o RCon[5]
            {0, 0, 1, 0, 0, 0, 0, 0},// este byte e o RCon[6]
            {0, 1, 0, 0, 0, 0, 0, 0},// este byte e o RCon[7]
            {1, 0, 0, 0, 0, 0, 0, 0},// este byte e o RCon[8]
            {0, 0, 0, 1, 1, 0, 1, 1},// este byte e o RCon[9]
            {0, 0, 1, 1, 0, 1, 1, 0},// este byte e o RCon[10]
            {0, 1, 1, 0, 1, 1, 0, 0},// este byte e o RCon[11]
            {1, 1, 0, 1, 1, 0, 0, 0},// este byte e o RCon[12]
            {1, 0, 1, 0, 1, 0, 1, 1},// este byte e o RCon[13]
            {0, 1, 0, 0, 1, 1, 0, 1},// este byte e o RCon[14]
            {1, 0, 1, 1, 0, 1, 1, 0},// este byte e o RCon[15]
            {0, 1, 1, 1, 0, 1, 1, 1},// este byte e o RCon[16]
            {1, 1, 1, 0, 1, 1, 1, 0},// este byte e o RCon[17]
        };//foram cradas até o r_con 17 para possibilitar 17 iteracoes do Alpha

        for (j = 0; j < 128; j++) { // atribui a chave aa primeira sub-chave        
            XK[0][j] = KEY[j];
        }
        for (i = 1; i < Nr; i++) {// i do FIPS para chave do round i. no ARK inicial i=0.
            for (c = 0; c < 8; c++) {//atribui a word W[i-1,3] a temp
                temp1[c] = XK[i - 1][c + 96];
                temp2[c] = XK[i - 1][c + 104];
                temp3[c] = XK[i - 1][c + 112];
                temp4[c] = XK[i - 1][c + 120];
            }//fim do for c
            temptemp = temp1;
            temp1 = temp2;
            temp2 = temp3;
            temp3 = temp4;
            temp4 = temptemp;//ROTWORD 
            //BYTESUB WORD
            temp1 = nAlpha(temp1, 0);
            temp2 = nAlpha(temp2, 0);
            temp3 = nAlpha(temp3, 0);
            temp4 = nAlpha(temp4, 0);
            //fim de BYTESUB WORD
            for (c = 0; c < 8; c++) {//soma RCon e faz XOR para gerar W[i,0],
            // que é a primeira WORD(de 32 bits) da sub-chave i
                temp1[c] = (temp1[c] + RCON[i][c]) % 2;
                XK[i][c] = (temp1[c] + XK[i - 1][c]) % 2;
                XK[i][c + 8] = (temp2[c] + XK[i - 1][c + 8]) % 2;
                XK[i][c + 16] = (temp3[c] + XK[i - 1][c + 16]) % 2;
                XK[i][c + 24] = (temp4[c] + XK[i - 1][c + 24]) % 2;
            }
            for (j = 1; j < 4; j++) {//para gerar as WORDS W[i,1],W[i,2],W[i,3]
                for (c = 0; c < 32; c++) {//
                    c2 = j * 32 + c;
                    XK[i][c2] = (XK[i - 1][c2] + XK[i][c2 - 32]) % 2;
                }//fim do for c
            }//fim do for j
        }//fim do for i
        return XK;
    }// ***************** fim do metodo expand key ************************
    
   /***********************************************************************
    *****           metodo nAlpha = (BYTESUB-rijndael)              ******
           argumento = baite bin                            ******
           retorna = baite bin                              ******
    ***********************************************************************/
    
    public static int[] nAlpha(int[] xy, int delta_linha) {//byte xy e oque sera substituido por zw
        int lin, col, substituto;
        int BS_decimal[][] = {
            {99, 124, 119, 123, 242, 107, 111, 197, 48, 1, 103, 43, 254, 215, 171, 118},
            {202, 130, 201, 125, 250, 89, 71, 240, 173, 212, 162, 175, 156, 164, 114, 192},
            {183, 253, 147, 38, 54, 63, 247, 204, 52, 165, 229, 241, 113, 216, 49, 21},
            {4, 199, 35, 195, 24, 150, 5, 154, 7, 18, 128, 226, 235, 39, 178, 117},
            {9, 131, 44, 26, 27, 110, 90, 160, 82, 59, 214, 179, 41, 227, 47, 132},
            {83, 209, 0, 237, 32, 252, 177, 91, 106, 203, 190, 57, 74, 76, 88, 207},
            {208, 239, 170, 251, 67, 77, 51, 133, 69, 249, 2, 127, 80, 60, 159, 168},
            {81, 163, 64, 143, 146, 157, 56, 245, 188, 182, 218, 33, 16, 255, 243, 210},
            {205, 12, 19, 236, 95, 151, 68, 23, 196, 167, 126, 61, 100, 93, 25, 115},
            {96, 129, 79, 220, 34, 42, 144, 136, 70, 238, 184, 20, 222, 94, 11, 219},
            {224, 50, 58, 10, 73, 6, 36, 92, 194, 211, 172, 98, 145, 149, 228, 121},
            {231, 200, 55, 109, 141, 213, 78, 169, 108, 86, 244, 234, 101, 122, 174, 8},
            {186, 120, 37, 46, 28, 166, 180, 198, 232, 221, 116, 31, 75, 189, 139, 138},
            {112, 62, 181, 102, 72, 3, 246, 14, 97, 53, 87, 185, 134, 193, 29, 158},
            {225, 248, 152, 17, 105, 217, 142, 148, 155, 30, 135, 233, 206, 85, 40, 223},
            {140, 161, 137, 13, 191, 230, 66, 104, 65, 153, 45, 15, 176, 84, 187, 22},};
        
        lin = xy[0] * 8 + xy[1] * 4 + xy[2] * 2 + xy[3];//clacula linha de entrada na caixa  (caso hexa)
        lin = (lin + delta_linha) % 16;
        
        col = xy[4] * 8 + xy[5] * 4 + xy[6] * 2 + xy[7];//calcula coluna de entrada na caixa (caso hexa)
        substituto = BS_decimal[lin][col];
        int zw[] = ByteConversion.CG2a8(substituto);
        return zw;
    }// ******************** fim do metodo SUBSTITUICAO *********************
    
    /****************************************************
     **********     metodo lAlpha                 ******
    obs: foi implementado bit a bit ******
 argumento = int[64] binario        ******
 retorna = int[64] binario          ******
     ****************************************************/
    public static int[] lAlpha(int e[]) {//
        int s[] = new int[64];
        s[20] = (e[62] + e[47] + e[11] + e[4] + e[30] + e[61] + e[52]) % 2;
        s[47] = (e[20] + e[35] + e[45] + e[29] + e[18] + e[34] + e[53]) % 2;
        s[11] = (e[20] + e[10] + e[59] + e[3] + e[16] + e[57] + e[51]) % 2;
        s[4] = (e[20] + e[40] + e[7] + e[32] + e[24] + e[8] + e[31]) % 2;
        s[30] = (e[20] + e[22] + e[37] + e[9] + e[54] + e[2] + e[44]) % 2;
        s[61] = (e[20] + e[60] + e[1] + e[38] + e[46] + e[50] + e[63]) % 2;
        s[52] = (e[20] + e[19] + e[25] + e[15] + e[5] + e[56] + e[43]) % 2;
        s[35] = (e[47] + e[28] + e[36] + e[21] + e[14] + e[48] + e[41]) % 2;
        s[45] = (e[47] + e[49] + e[27] + e[0] + e[33] + e[13] + e[17]) % 2;
        s[29] = (e[47] + e[58] + e[39] + e[12] + e[23] + e[26] + e[6]) % 2;
        s[18] = (e[47] + e[55] + e[42] + e[62] + e[37] + e[5] + e[53]) % 2;
        s[34] = (e[47] + e[8] + e[14] + e[3] + e[63] + e[50] + e[32]) % 2;
        s[53] = (e[47] + e[15] + e[48] + e[60] + e[2] + e[33] + e[22]) % 2;
        s[10] = (e[11] + e[59] + e[12] + e[38] + e[55] + e[1] + e[23]) % 2;
        s[59] = (e[11] + e[56] + e[0] + e[49] + e[9] + e[39] + e[19]) % 2;
        s[3] = (e[11] + e[6] + e[57] + e[51] + e[13] + e[34] + e[43]) % 2;
        s[16] = (e[11] + e[7] + e[36] + e[17] + e[24] + e[58] + e[54]) % 2;
        s[57] = (e[11] + e[10] + e[31] + e[32] + e[42] + e[21] + e[63]) % 2;
        s[51] = (e[11] + e[55] + e[12] + e[2] + e[40] + e[26] + e[9]) % 2;
        s[40] = (e[4] + e[33] + e[49] + e[16] + e[60] + e[3] + e[62]) % 2;
        s[7] = (e[4] + e[53] + e[25] + e[38] + e[23] + e[14] + e[1]) % 2;
        s[32] = (e[4] + e[46] + e[56] + e[27] + e[6] + e[39] + e[51]) % 2;
        s[24] = (e[4] + e[15] + e[21] + e[41] + e[28] + e[50] + e[44]) % 2;
        s[8] = (e[4] + e[36] + e[5] + e[16] + e[59] + e[10] + e[17]) % 2;
        s[31] = (e[4] + e[25] + e[58] + e[37] + e[48] + e[0] + e[13]) % 2;
        s[22] = (e[30] + e[44] + e[19] + e[34] + e[7] + e[8] + e[57]) % 2;
        s[37] = (e[30] + e[40] + e[54] + e[27] + e[41] + e[9] + e[60]) % 2;
        s[9] = (e[30] + e[26] + e[5] + e[48] + e[38] + e[49] + e[12]) % 2;
        s[54] = (e[30] + e[58] + e[1] + e[33] + e[17] + e[31] + e[46]) % 2;
        s[2] = (e[30] + e[22] + e[28] + e[3] + e[13] + e[56] + e[42]) % 2;
        s[44] = (e[30] + e[36] + e[53] + e[16] + e[63] + e[43] + e[14]) % 2;
        s[60] = (e[61] + e[19] + e[55] + e[32] + e[24] + e[0] + e[62]) % 2;
        s[1] = (e[61] + e[37] + e[21] + e[10] + e[54] + e[41] + e[25]) % 2;
        s[38] = (e[61] + e[2] + e[57] + e[34] + e[7] + e[15] + e[51]) % 2;
        s[46] = (e[61] + e[27] + e[44] + e[23] + e[39] + e[42] + e[22]) % 2;
        s[50] = (e[61] + e[24] + e[6] + e[59] + e[8] + e[32] + e[14]) % 2;
        s[63] = (e[61] + e[60] + e[40] + e[16] + e[25] + e[0] + e[54]) % 2;
        s[19] = (e[52] + e[50] + e[2] + e[63] + e[37] + e[13] + e[43]) % 2;
        s[25] = (e[52] + e[22] + e[28] + e[53] + e[9] + e[59] + e[31]) % 2;
        s[15] = (e[52] + e[46] + e[39] + e[18] + e[55] + e[6] + e[8]) % 2;
        s[5] = (e[52] + e[23] + e[33] + e[49] + e[58] + e[7] + e[26]) % 2;
        s[56] = (e[52] + e[41] + e[1] + e[57] + e[27] + e[36] + e[19]) % 2;
        s[43] = (e[52] + e[44] + e[51] + e[12] + e[42] + e[62] + e[21]) % 2;
        s[28] = (e[35] + e[34] + e[31] + e[3] + e[48] + e[10] + e[46]) % 2;
        s[36] = (e[35] + e[5] + e[50] + e[38] + e[15] + e[26] + e[17]) % 2;
        s[21] = (e[35] + e[56] + e[18] + e[39] + e[57] + e[53] + e[24]) % 2;
        s[14] = (e[35] + e[1] + e[12] + e[43] + e[8] + e[59] + e[40]) % 2;
        s[48] = (e[35] + e[28] + e[7] + e[23] + e[49] + e[37] + e[42]) % 2;
        s[41] = (e[35] + e[10] + e[0] + e[51] + e[25] + e[34] + e[16]) % 2;
        s[49] = (e[45] + e[62] + e[17] + e[5] + e[50] + e[31] + e[58]) % 2;
        s[27] = (e[45] + e[13] + e[44] + e[36] + e[22] + e[38] + e[60]) % 2;
        s[0] = (e[45] + e[43] + e[9] + e[2] + e[48] + e[26] + e[33]) % 2;
        s[33] = (e[45] + e[6] + e[55] + e[19] + e[28] + e[41] + e[63]) % 2;
        s[13] = (e[45] + e[14] + e[24] + e[32] + e[40] + e[54] + e[21]) % 2;
        s[17] = (e[45] + e[15] + e[3] + e[56] + e[18] + e[46] + e[5]) % 2;
        s[58] = (e[29] + e[60] + e[27] + e[13] + e[34] + e[49] + e[15]) % 2;
        s[39] = (e[29] + e[42] + e[17] + e[3] + e[59] + e[26] + e[33]) % 2;
        s[12] = (e[29] + e[48] + e[0] + e[31] + e[46] + e[22] + e[56]) % 2;
        s[23] = (e[29] + e[14] + e[55] + e[36] + e[53] + e[6] + e[9]) % 2;
        s[26] = (e[29] + e[19] + e[37] + e[58] + e[24] + e[44] + e[25]) % 2;
        s[6] = (e[29] + e[21] + e[41] + e[7] + e[57] + e[51] + e[32]) % 2;
        s[55] = (e[18] + e[12] + e[62] + e[27] + e[38] + e[10] + e[2]) % 2;
        s[42] = (e[18] + e[43] + e[16] + e[50] + e[23] + e[54] + e[1]) % 2;
        s[62] = (e[18] + e[20] + e[40] + e[28] + e[63] + e[39] + e[8]) % 2;
        return s;
    }// ************    fim do metodo Lalpha    *****************
    
    /***********************************************************************
     *****          metodo hexa - converte bin-hexa                   ******
     **********         argumento = int[4] binario                    ******
     ***********    retorna = um caracter hexa                        ******
     **********************************************************************/
    public static String hexa(int bin[]){
        String [] Simbolos = {"0","1","2","3","4","5","6","7","8","9","a","b","c","d","e","f"};
        String h= Simbolos[(8*bin[0]+4*bin[1]+2*bin[2]+bin[3])];
        return h;
    }// ******************** fim do metodo hexa ****************************

    public static int[] alpha(int MSG[], int KEY[], int cifra, int Nr) {
        int blockSize = 128;
        MSG = padd(MSG, blockSize);
        int[] result = new int[MSG.length];        
        int qtdBlocos = MSG.length/blockSize;

        for (int i = 0; i < qtdBlocos; i++) {
            int[] bloco = cifraBloco(getBlock(MSG, i, blockSize), KEY, cifra, Nr);
            System.arraycopy(bloco, 0, result, blockSize*i, blockSize);
        }
        return result;
    }
    
    
    /**
     * Retrieves the nth block of the given text, the blockSize is measured in bites
     *  example:
     *  int array[] = {0,1,1,0,1,0,0,0,0,1,1,0,0,1,0,1,0,1,1,0,1,1,0,0,0,1,1,0,1,1,0,0,0,1,1,0,1,1,1,1,0,0,1,0,0,0,0,1};
     *  int [] block = getBlock(array, 0, 24);
     *  block would be equivalent to the following declaration:
     *  int block[] = {0,1,1,0,1,0,0,0,0,1,1,0,0,1,0,1,0,1,1,0,1,1,0,0};
     *  
     * @param MSG the int array to be retrieve the block from
     * @param desiredBlock the index of the block (starting from 0)
     * @param blockSize the size of the block
     * @return the whole block extracted from MSG
     */
    public static int[] getBlock(int[] MSG, int desiredBlock, int blockSize){
        int[] block = new int[blockSize];
        System.arraycopy(MSG, desiredBlock*blockSize, block, 0, blockSize);
        return block;
    }
    
    
    public static String printB(int[] binario){
        String result = "";
        for (int i=0; i<binario.length;i++){
            result+=binario[i];
            if (i%8==7) result+=" ";
        }
        return result;
    }
    
    
    /**
     * Padd the received text so its size will match the block size.
     * @param txt text to be padded
     * @param blockSize the size that txt should be padded to reach
     * @return the padded text, the text will be padded with spaces (byte 00100000) in ASCII
     */
    private static int[] padd(int[] txt, int blockSize){
        if (!(txt.length%blockSize==0)){
            int posicoesFaltando = blockSize-txt.length%blockSize;
            int[] novoArray = new int[txt.length+posicoesFaltando];
            System.arraycopy(txt, 0, novoArray, 0, txt.length);
            for(int i=8;i<posicoesFaltando;i+=8){
                novoArray[txt.length+i+0]=0;
                novoArray[txt.length+i+1]=0;
                novoArray[txt.length+i+2]=1;
                novoArray[txt.length+i+3]=0;
                novoArray[txt.length+i+4]=0;
                novoArray[txt.length+i+5]=0;
                novoArray[txt.length+i+6]=0;
                novoArray[txt.length+i+7]=0;
            }
            return novoArray;
        } else {
            return txt;
        }
    }
}
