import java.awt.List;
import java.io.PrintWriter;
import java.util.HashMap;

import sketch.compiler.ast.core.FEReplacer;
//import sketch.compiler.ast.core.Package;
import sketch.compiler.ast.core.Function;
import sketch.compiler.ast.core.exprs.*;
import sketch.compiler.ast.core.stmts.*;
import sketch.util.annot.CodeGenerator;

/**
 * CodeGenerator to generate snippets of Java code to be embedded back
 * into the input JSketch to produce runnable synthesized Java code.
 * 
 * As java-sketch adopts generator and choice syntaxes from Sketch. It is
 * hard to rebuild runnable Java code from Sketch output merely from hole
 * values, since holes are ambiguous when these syntaxes are used and internal
 * conversion of Sketch data structures would be needed to resolve these
 * results. Thus it is more preferable to generate Java code in small snippets
 * (ideally per function/method) and embed snippets back to java sketch source
 * to produce whole code.
 * 
 * The output of this CodeGenerator is expected to be used with an external
 * post-processor which could embed the generated function/method snippets back.
 */

@CodeGenerator
public class JavaCode extends FEReplacer {

  final PrintWriter out;

  HashMap<String, List<String>> func_impl;

  public JavaCode() {
    out = new PrintWriter(System.out);
    func_impl = new HashMap<String, List<String>>();
  }

  private String cur_pkg;

  @Override
  public Object visitPackage(Package spec) {
    cur_pkg = spec.getName();
    Object rtn_obj = super.visitPackage(spec);

    return rtn_obj;
  }

  private String cur_func;
  private List<String> cur_func_stmt_list;

  @Override
  public Object visitFunction(Function func) {
    cur_func = func.getName();
    cur_func_stmt_list = new ArrayList<String>();
    func_impl.put(cur_pkg + "::" + cur_func, cur_func_stmt_list);
    return super.visitFunction(func);
  }

  void printInfo(Object obj) {
    String typ = obj.getClass().getSimpleName();
    //out.println(cur_pkg + "," + cur_func + "," + typ + "," + obj.toString());
    out.println(cur_func + "," + typ + "," + obj.toString());
    out.flush();
  }

// to learn AST.Expression
/*
  @Override
  public Expression doExpression(Expression exp) {
    out.println(cur_func + "," + exp.getClass().getName() + "," + exp.toString());
    out.flush();
    return super.doExpression(exp);
  }
*/

  @Override
  public Object visitExprBinary(ExprBinary exp) {
    printInfo(exp);
    return super.visitExprBinary(exp);
  }

// seems never visited because all holes are already resolved and replaced
/* 
  @Override
  public Object visitExprStar(ExprStar exp) {
    // how to retrieve the value associated with this hole?
    out.println(cur_func + "," + exp.getSname() + ",");
    return super.visitExprStar(exp);
  }
*/

  @Override
  public Object visitStmtAssign(StmtAssign stmt) {
    printInfo(stmt);
    return super.visitStmtAssign(stmt);
  }

  @Override
  public Object visitStmtVarDecl(StmtVarDecl stmt) {
    printInfo(stmt);
    return super.visitStmtVarDecl(stmt);
  }

}
