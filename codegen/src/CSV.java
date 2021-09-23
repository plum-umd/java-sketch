import java.io.PrintWriter;

import sketch.compiler.ast.core.FEReplacer;
import sketch.compiler.ast.core.FENode;
import sketch.compiler.ast.core.FEContext;
//import sketch.compiler.ast.core.Package;
import sketch.compiler.ast.core.Function;
import sketch.compiler.ast.core.exprs.*;
import sketch.compiler.ast.core.stmts.*;
import sketch.util.annot.CodeGenerator;

@CodeGenerator
public class CSV extends FEReplacer {

  final PrintWriter out;

  public CSV() {
    out = new PrintWriter(System.out);
  }

/*
  private String cur_pkg;

  @Override
  public Object visitPackage(Package spec) {
    cur_pkg = spec.getName();
    return super.visitPackage(spec);
  }
*/

  private String cur_func;

  @Override
  public Object visitFunction(Function func) {
    cur_func = func.getName();
    if (func.getBody().isBlock()) {
      for (Statement stmt: ((StmtBlock)func.getBody()).getStmts()){
        printInfo(stmt);
      }
    }
    return super.visitFunction(func);
  }

  void printInfo(Object obj) {
    String typ = obj.getClass().getSimpleName();
    FEContext ctx = ((FENode)obj).getCx();
    //out.println(cur_pkg + "," + cur_func + "," + typ + "," + obj.toString());
    out.println("\"" + cur_func + "\"," 
                + "\"" + typ + "\","
                + "\"" + ctx.getFileName() + ":" + Integer.toString(ctx.getLineNumber()) + ":" + Integer.toString(ctx.getColumnNumber()) + "\","
                + "\"" + obj.toString() + "\"");
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

  // @Override
  // public Object visitExprBinary(ExprBinary exp) {
  //   printInfo(exp);
  //   return super.visitExprBinary(exp);
  // }

// seems never visited because all holes are already resolved and replaced
/* 
  @Override
  public Object visitExprStar(ExprStar exp) {
    // how to retrieve the value associated with this hole?
    out.println(cur_func + "," + exp.getSname() + ",");
    return super.visitExprStar(exp);
  }
*/

  // @Override
  // public Object visitStmtAssign(StmtAssign stmt) {
  //   printInfo(stmt);
  //   return super.visitStmtAssign(stmt);
  // }

  // @Override
  // public Object visitStmtVarDecl(StmtVarDecl stmt) {
  //   printInfo(stmt);
  //   return super.visitStmtVarDecl(stmt);
  // }

}
