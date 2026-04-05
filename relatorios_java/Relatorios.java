import javax.swing.JOptionPane;;
/*
 * Classe JOptionPane (javax.swing)
 * Métodos Estáticos:
 * .showMessageDialog(null,"mensagem");
 * .showInputDialog("mensagem");
 */
public class Relatorios
{ 
   public static void main(String[] args) 
   {
      String nome1, nome2;
      float peso1, peso2, altura1, altura2;
      float imc1, imc2;
      String classifica1, classifica2;
      
      data = date.parseFloat(JOptionPane.showInputDialog(" Data "));
      ativo = JOptionPane.showInputDialog(" Ativo");
      classe = JOptionPane.showInputDialog(" Classe");
      quant= int.parseFloat(JOptionPane.showInputDialog("Quantidade"));
      proventos = Float.parseFloat(JOptionPane.showInputDialog(" Proventos") );
      compra = Float.parseFloat(JOptionPane.showInputDialog("Preço de Compra") );
      venda = Float.parseFloat(JOptionPane.showInputDialog("Preço de venda") );

      total1 = (float) (quant*Math.pow(compra, 2));
      total2 = (float) (quant*Math.pow(venda, 2));
       
      
         JOptionPane.showMessageDialog(null, "Compras \"total1"\);
       JOptionPane.showMessageDialog(null, "Vendas \"total2"\);
   }
}
