/*
 * To change this license header, choose License Headers in Project Properties.
 * To change this template file, choose Tools | Templates
 * and open the template in the editor.
 */

package br.eb.ime.alpha.conversion;

/**
 *
 * @author yurifw
 */
public class ByteConversion {

    /***********************************************************************
     *****        metodo CG2a8- converte inteiro ate 255 em polinomio ******
     *****                          argumento = int                   ******
     *****              retorna = um polinomio do CG(2^8)             ******
     **********************************************************************/
    public static int[] CG2a8(int inteiro) {
        int[] polinomio = {0, 0, 0, 0, 0, 0, 0, 0};
        int p2 = 128;
        for (int i = 0; i < 8; i++) {
            if (inteiro > (p2 - 1)) {
                polinomio[i] = 1;
                inteiro = inteiro - p2;
            }
            p2 = p2 / 2;
        }
        return polinomio;
    }

    /**
     * Transforms a String int an array of ints.
     * Each position of the array represents a bit of the String.
     * so for an input "1a", the expected result is an array which would be equivalent to the declaration:
     * int[] result = {0,0,1,1,0,0,0,1,0,1,1,0,0,0,0,1};
     * @param s String to be transformed
     * @return an array of int, each position of the array is either a 0 or a 1
     */
    public static int[] stringToInt(String s) {
        int[] result = new int[8 * s.length()];
        byte[] bytes = s.getBytes();
        for (int i = 0; i < s.length(); i++) {
            System.arraycopy(CG2a8(bytes[i]), 0, result, i * 8, 8);
        }
        return result;
    }

    /**
     * Converts an array of bites in the form of string to an array of int representing an array of bites
     * @param string array of bits in the form of String
     * @return array of bits in the form of int[]
     */
    public static int[] binaryStringToInt(String string) {
        String cropped = string.replaceAll(" ", "");
        int[] result = new int[cropped.length()];
        for (int i = 0; i < cropped.length(); i++) {
            result[i] = cropped.charAt(i) == '1' ? 1 : 0;
        }
        return result;
    }

    /**
     * Inverse of @stringToInt.
     * Changes an array of bits into a String.
     * So for an intput:
     * int[] array = {0,0,1,1,0,0,0,1,0,1,1,0,0,0,0,1};
     * the expected result is : "1a"
     * @param array the array of bits to be converted into a string
     * @return a String converted from an array of bits
     */
    public static String intToString(int[] array) {
        String result = "";
        int[] bytes = new int[array.length / 8];
        for (int i = 0; i < array.length; i += 8) {
            bytes[i / 8] = (array[i + 0]) | bytes[i / 8] << 1;
            bytes[i / 8] = (array[i + 1]) | bytes[i / 8] << 1;
            bytes[i / 8] = (array[i + 2]) | bytes[i / 8] << 1;
            bytes[i / 8] = (array[i + 3]) | bytes[i / 8] << 1;
            bytes[i / 8] = (array[i + 4]) | bytes[i / 8] << 1;
            bytes[i / 8] = (array[i + 5]) | bytes[i / 8] << 1;
            bytes[i / 8] = (array[i + 6]) | bytes[i / 8] << 1;
            bytes[i / 8] = (array[i + 7]) | bytes[i / 8] << 1;
            result += (char) bytes[i / 8];
        }
        return result;
    }
    
}
