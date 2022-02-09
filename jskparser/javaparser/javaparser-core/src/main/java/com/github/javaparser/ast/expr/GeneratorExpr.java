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

import java.util.List;

import com.github.javaparser.ast.visitor.GenericVisitor;
import com.github.javaparser.ast.visitor.VoidVisitor;

/**
 * @author Josh Reese
 */
public final class GeneratorExpr extends Expression {
    private boolean isHole;

    private List<Expression> exprs;

    private IntegerLiteralExpr width;

    public GeneratorExpr() {
    }

    public GeneratorExpr(int beginLine, int beginColumn, int endLine, int endColumn, boolean ishole, List<Expression> exprs, IntegerLiteralExpr width) {
        super(beginLine, beginColumn, endLine, endColumn);
	this.isHole = ishole;
	this.exprs = exprs;
    this.width = width;
    }

    @Override
    public <R, A> R accept(GenericVisitor<R, A> v, A arg) {
        return v.visit(this, arg);
    }
    
    @Override
    public <A> void accept(VoidVisitor<A> v, A arg) {
        v.visit(this, arg);
    }

    /**
     * Return whether or not this node is a hole
     *
     * @return whether or not this node is a hole (??)
     */
    public boolean getIsHole() {
        return isHole;
    }

    /**
     * Sets whether or not this node is a hole
     *
     * @return void
     */
    public void setIsHole(boolean ishole) {
        this.isHole = ishole;
    }

    /**
     * Return generator expression
     *
     * @return the generator expressions associated with this node ( {| ... |} )
     */
    public List<Expression> getExprs() {
        return exprs;
    }

    /**
     * Sets the expression for this generator
     *
     * @return void
     */
    public void setExprs(List<Expression> exprs) {
        this.exprs = exprs;
    }

    public void setWidth(IntegerLiteralExpr width) {
        this.width = width;
    }

    public IntegerLiteralExpr getWidth() {
        return width;
    }
}
