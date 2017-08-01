package jskparser;

import java.io.FileInputStream;
import java.io.OutputStream;
import java.io.FileOutputStream;
import java.io.IOException;
import java.io.FileNotFoundException;
import java.lang.Exception;
import java.util.HashMap;
import java.util.Map;

import com.github.javaparser.JavaParser;
import com.github.javaparser.ast.CompilationUnit;
import com.github.javaparser.ast.visitor.JsonVisitorAdapter;

import com.cedarsoftware.util.io.JsonWriter;

public class Jsonify {
    public static void main(String[] args) throws Exception {
        CompilationUnit cu;
        FileInputStream in = new FileInputStream(args[0]);

        try {
            cu = JavaParser.parse(in);
            try {
                FileOutputStream out = new FileOutputStream(args[1]);

                Map json_args = constructJsonArgMap();
                new JsonWriter(out, json_args).write(cu);

                try {
                    out.close();
                } catch (IOException e) {
                    throw e;
                }
            } catch (FileNotFoundException e) {
                throw e;
            } 
        } finally {
            in.close();
        }
    }

    private static Map constructJsonArgMap() {
        Map typeRewrites = new HashMap();
        typeRewrites.put("java.util.ArrayList","ArrayList");
        typeRewrites.put("java.util.LinkedList","LinkedList");

        typeRewrites.put("com.github.javaparser.ast.CompilationUnit","CompilationUnit");
        typeRewrites.put("com.github.javaparser.ast.ImportDeclaration","ImportDeclaration");
        typeRewrites.put("com.github.javaparser.ast.ImportDeclaration","ImportDeclaration");
        typeRewrites.put("com.github.javaparser.ast.TypeParameter","TypeParameter");
        typeRewrites.put("com.github.javaparser.ast.TypeArguments","TypeArguments");

        typeRewrites.put("com.github.javaparser.ast.body.ClassOrInterfaceDeclaration","ClassOrInterfaceDeclaration");
        typeRewrites.put("com.github.javaparser.ast.body.FieldDeclaration","FieldDeclaration");
        typeRewrites.put("com.github.javaparser.ast.body.MethodDeclaration","MethodDeclaration");
        typeRewrites.put("com.github.javaparser.ast.body.ConstructorDeclaration","ConstructorDeclaration");
        typeRewrites.put("com.github.javaparser.ast.body.Parameter","Parameter");
        typeRewrites.put("com.github.javaparser.ast.expr.IntegerLiteralExpr","IntegerLiteralExpr");
        typeRewrites.put("com.github.javaparser.ast.body.VariableDeclarator","VariableDeclarator");
        typeRewrites.put("com.github.javaparser.ast.type.PrimitiveType","PrimitiveType");
        typeRewrites.put("com.github.javaparser.ast.type.ReferenceType","ReferenceType");
        typeRewrites.put("com.github.javaparser.ast.type.ClassOrInterfaceType","ClassOrInterfaceType");
        typeRewrites.put("com.github.javaparser.ast.type.VoidType","VoidType");
        typeRewrites.put("com.github.javaparser.ast.body.EmptyMemberDeclaration","EmptyMemberDeclaration");
        typeRewrites.put("com.github.javaparser.ast.body.InitializerDeclaration","InitializerDeclaration");
        typeRewrites.put("com.github.javaparser.ast.body.AxiomDeclaration","AxiomDeclaration");
        typeRewrites.put("com.github.javaparser.ast.body.AxiomParameter","AxiomParameter");

        // Statements
        typeRewrites.put("com.github.javaparser.ast.stmt.BlockStmt","BlockStmt");
        typeRewrites.put("com.github.javaparser.ast.stmt.IfStmt","IfStmt");
        typeRewrites.put("com.github.javaparser.ast.stmt.ExpressionStmt","ExpressionStmt");
        typeRewrites.put("com.github.javaparser.ast.stmt.ReturnStmt","ReturnStmt");
        typeRewrites.put("com.github.javaparser.ast.stmt.AssertStmt","AssertStmt");
        typeRewrites.put("com.github.javaparser.ast.stmt.ForStmt","ForStmt");
        typeRewrites.put("com.github.javaparser.ast.stmt.ForeachStmt","ForeachStmt");
        typeRewrites.put("com.github.javaparser.ast.stmt.WhileStmt","WhileStmt");
        typeRewrites.put("com.github.javaparser.ast.stmt.EmptyStmt","EmptyStmt");
        typeRewrites.put("com.github.javaparser.ast.stmt.ContinueStmt","ContinueStmt");
        typeRewrites.put("com.github.javaparser.ast.stmt.BreakStmt","BreakStmt");
        typeRewrites.put("com.github.javaparser.ast.stmt.TryStmt","TryStmt");
        typeRewrites.put("com.github.javaparser.ast.stmt.CatchClause","CatchClause");
        typeRewrites.put("com.github.javaparser.ast.stmt.SwitchStmt","SwitchStmt");
        typeRewrites.put("com.github.javaparser.ast.stmt.SwitchEntryStmt","SwitchEntryStmt");
        typeRewrites.put("com.github.javaparser.ast.stmt.ExplicitConstructorInvocationStmt","ExplicitConstructorInvocationStmt");
        typeRewrites.put("com.github.javaparser.ast.stmt.AssumeStmt","AssumeStmt");
        typeRewrites.put("com.github.javaparser.ast.stmt.MinrepeatStmt","MinrepeatStmt");
        typeRewrites.put("com.github.javaparser.ast.stmt.ThrowStmt","ThrowStmt");
	
        // Expressions
        typeRewrites.put("com.github.javaparser.ast.expr.AssignExpr","AssignExpr");
        typeRewrites.put("com.github.javaparser.ast.expr.VariableDeclarationExpr","VariableDeclarationExpr");
        typeRewrites.put("com.github.javaparser.ast.expr.UnaryExpr","UnaryExpr");
        typeRewrites.put("com.github.javaparser.ast.expr.BinaryExpr","BinaryExpr");
        typeRewrites.put("com.github.javaparser.ast.expr.NameExpr","NameExpr");
        typeRewrites.put("com.github.javaparser.ast.expr.MethodCallExpr","MethodCallExpr");
        typeRewrites.put("com.github.javaparser.ast.expr.GeneratorExpr","GeneratorExpr");
        typeRewrites.put("com.github.javaparser.ast.expr.ObjectCreationExpr","ObjectCreationExpr");
        typeRewrites.put("com.github.javaparser.ast.expr.FieldAccessExpr","FieldAccessExpr");
        typeRewrites.put("com.github.javaparser.ast.expr.ThisExpr","ThisExpr");
        typeRewrites.put("com.github.javaparser.ast.expr.SuperExpr","SuperExpr");
        typeRewrites.put("com.github.javaparser.ast.expr.EnclosedExpr","EnclosedExpr");
        typeRewrites.put("com.github.javaparser.ast.expr.ArrayCreationExpr","ArrayCreationExpr");
        typeRewrites.put("com.github.javaparser.ast.expr.ArrayInitializerExpr","ArrayInitializerExpr");
        typeRewrites.put("com.github.javaparser.ast.expr.ArrayAccessExpr","ArrayAccessExpr");
        typeRewrites.put("com.github.javaparser.ast.expr.StringLiteralExpr","StringLiteralExpr");
        typeRewrites.put("com.github.javaparser.ast.expr.NullLiteralExpr","NullLiteralExpr");
        typeRewrites.put("com.github.javaparser.ast.expr.DoubleLiteralExpr","DoubleLiteralExpr");
	typeRewrites.put("com.github.javaparser.ast.expr.BooleanLiteralExpr","BooleanLiteralExpr");
	typeRewrites.put("com.github.javaparser.ast.expr.LongLiteralExpr","LongLiteralExpr");
        typeRewrites.put("com.github.javaparser.ast.expr.QualifiedNameExpr","QualifiedNameExpr");
        typeRewrites.put("com.github.javaparser.ast.expr.ConditionalExpr","ConditionalExpr");
        typeRewrites.put("com.github.javaparser.ast.expr.CastExpr","CastExpr");
	typeRewrites.put("com.github.javaparser.ast.expr.CharLiteralExpr","CharLiteralExpr");
	typeRewrites.put("com.github.javaparser.ast.expr.InstanceOfExpr","InstanceOfExpr");
	typeRewrites.put("com.github.javaparser.ast.expr.AnnotationExpr","AnnotationExpr");
	typeRewrites.put("com.github.javaparser.ast.expr.SingleMemberAnnotationExpr","SingleMemberAnnotationExpr");
	typeRewrites.put("com.github.javaparser.ast.expr.MarkerAnnotationExpr","MarkerAnnotationExpr");
	typeRewrites.put("com.github.javaparser.ast.expr.NormalAnnotationExpr","NormalAnnotationExpr");
	
	// Comments
        typeRewrites.put("com.github.javaparser.ast.comments.Comment","Comment");
	typeRewrites.put("com.github.javaparser.ast.comments.JavadocComment","JavadocComment");
	typeRewrites.put("com.github.javaparser.ast.comments.LineComment","LineComment");
	typeRewrites.put("com.github.javaparser.ast.comments.BlockComment","BlockComment");

        Map jsonArgs = new HashMap();
        jsonArgs.put(JsonWriter.PRETTY_PRINT, true);
        jsonArgs.put(JsonWriter.SHORT_META_KEYS, true);
        jsonArgs.put(JsonWriter.TYPE_NAME_MAP, typeRewrites);

        return jsonArgs;
    }
}
