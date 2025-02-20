/*
 * Copyright (C) 2007-2010 Júlio Vilmar Gesser.
 * Copyright (C) 2011, 2013-2015 The JavaParser Team.
 *
 * This file is part of JavaParser.
 * 
 * JavaParser can be used either under the terms of
 * a) the GNU Lesser General Public License as published by
 *     the Free Software Foundation, either version 3 of the License, or
 *     (at your option) any later version.
 * b) the terms of the Apache License 
 *
 * You should have received a copy of both licenses in LICENCE.LGPL and
 * LICENCE.APACHE. Please refer to those files for details.
 *
 * JavaParser is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU Lesser General Public License for more details.
 */
 
package com.github.javaparser.ast.expr;

import com.github.javaparser.ast.type.Type;
import com.github.javaparser.ast.visitor.GenericVisitor;
import com.github.javaparser.ast.visitor.VoidVisitor;

import java.util.List;

import static com.github.javaparser.ast.internal.Utils.*;

/**
 * @author Julio Vilmar Gesser
 */
public final class MethodCallExpr extends Expression {

	private Expression scope;

	private List<Type> typeArgs;

	private NameExpr name;

	private List<Expression> args;

        private boolean pure = true;

	public MethodCallExpr() {
	}

	public MethodCallExpr(final Expression scope, final String name) {
		setScope(scope);
		setName(name);
	}

	public MethodCallExpr(final Expression scope, final String name, final List<Expression> args) {
		setScope(scope);
		setName(name);
		setArgs(args);
	}

	public MethodCallExpr(final int beginLine, final int beginColumn, final int endLine, final int endColumn,
			final Expression scope, final List<Type> typeArgs, final String name, final List<Expression> args) {
		super(beginLine, beginColumn, endLine, endColumn);
		setScope(scope);
		setTypeArgs(typeArgs);
		setName(name);
		setArgs(args);
	}

	public MethodCallExpr(final int beginLine, final int beginColumn, final int endLine, final int endColumn,
			      final Expression scope, final List<Type> typeArgs, final String name, final List<Expression> args, boolean bang) {
		super(beginLine, beginColumn, endLine, endColumn);
		setScope(scope);
		setTypeArgs(typeArgs);
		setName(name);
		setArgs(args);
		setPure(!bang);
	}
    
	@Override public <R, A> R accept(final GenericVisitor<R, A> v, final A arg) {
		return v.visit(this, arg);
	}

	@Override public <A> void accept(final VoidVisitor<A> v, final A arg) {
		v.visit(this, arg);
	}

        public boolean getPure() {
	return pure;
        }
    
	public List<Expression> getArgs() {
        args = ensureNotNull(args);
        return args;
	}

	public String getName() {
		return name.getName();
	}

	public NameExpr getNameExpr() {
		return name;
	}

	public Expression getScope() {
		return scope;
	}

	public List<Type> getTypeArgs() {
        typeArgs = ensureNotNull(typeArgs);
        return typeArgs;
	}

        public void setPure(final boolean pure) {
	    this.pure = pure;
        }
    
	public void setArgs(final List<Expression> args) {
		this.args = args;
		setAsParentNodeOf(this.args);
	}

	public void setName(final String name) {
		this.name = new NameExpr(name);
	}

	public void setNameExpr(NameExpr name) {
		this.name = name;
	}

	public void setScope(final Expression scope) {
		this.scope = scope;
		setAsParentNodeOf(this.scope);
	}

	public void setTypeArgs(final List<Type> typeArgs) {
		this.typeArgs = typeArgs;
		setAsParentNodeOf(this.typeArgs);
	}
}
