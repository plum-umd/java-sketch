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

import com.github.javaparser.ast.visitor.GenericVisitor;
import com.github.javaparser.ast.visitor.VoidVisitor;

/**
 * @author Julio Vilmar Gesser
 */
public final class ArrayRangeAccessExpr extends Expression {

    private Expression name;

    private Expression indexStart;
    private Expression subLen;

    public ArrayRangeAccessExpr() {
    }

    public ArrayRangeAccessExpr(Expression name, Expression indexStart, Expression subLen) {
        setName(name);
        setIndexStart(indexStart);
        setSubLen(subLen);
    }

    public ArrayRangeAccessExpr(int beginLine, int beginColumn, int endLine, int endColumn, Expression name, Expression indexStart, Expression subLen) {
        super(beginLine, beginColumn, endLine, endColumn);
        setName(name);
        setIndexStart(indexStart);
        setSubLen(subLen);
    }

    @Override
    public <R, A> R accept(GenericVisitor<R, A> v, A arg) {
        return v.visit(this, arg);
    }

    @Override
    public <A> void accept(VoidVisitor<A> v, A arg) {
        v.visit(this, arg);
    }

    public Expression getIndexStart() {
        return indexStart;
    }

    public Expression getSubLen() {
        return subLen;
    }

    public Expression getName() {
        return name;
    }

    public void setIndexStart(Expression indexStart) {
        this.indexStart = indexStart;
		setAsParentNodeOf(this.indexStart);
    }

    public void setSubLen(Expression subLen) {
        this.subLen = subLen;
		setAsParentNodeOf(this.subLen);
    }

    public void setName(Expression name) {
        this.name = name;
		setAsParentNodeOf(this.name);
    }
}
