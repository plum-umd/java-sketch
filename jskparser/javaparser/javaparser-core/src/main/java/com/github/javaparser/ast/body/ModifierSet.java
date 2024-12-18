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

/* Class access:
 * ACC_PUBLIC       0x0001
 * ACC_FINAL        0x0010
 * ACC_SUPER        0x0020
 * ACC_INTERFACE    0x0200
 * ACC_ABSTRACT     0x0400
 * ACC_SYNTHETIC    0x1000
 * ACC_ANNOTATION   0x2000
 * ACC_ENUM         0x4000 
 */

/* Field access:
 * ACC_PUBLIC       0x0001
 * ACC_PRIVATE      0x0002
 * ACC_PROTECTED    0x0004
 * ACC_STATIC       0x0008
 * ACC_FINAL        0x0010
 * ACC_VOLATILE     0x0040
 * ACC_TRANSIENT    0x0080
 * ACC_SYNTHETIC    0x1000
 * ACC_ENUM         0x4000
 */

/* Method access:
 * ACC_PUBLIC       0x0001
 * ACC_PRIVATE      0x0002
 * ACC_PROTECTED    0x0004
 * ACC_STATIC       0x0008
 * ACC_FINAL        0x0010
 * ACC_SYNCHRONIZED 0x0020
 * ACC_BRIDGE       0x0040
 * ACC_VARARGS      0x0080
 * ACC_NATIVE       0x0100
 * ACC_ABSTRACT     0x0400
 * ACC_STRICT       0x0800
 * ACC_SYNTHETIC    0x1000
 */

package com.github.javaparser.ast.body;

import com.github.javaparser.ast.AccessSpecifier;

import java.lang.reflect.Modifier;

/**
 * Class to hold modifiers.<br>
 * The modifier constants declared here holds equivalent values to
 * {@link Modifier} constants.
 */
public final class ModifierSet {
    
    /* Definitions of the bits in the modifiers field.  */

    public static final int PUBLIC = Modifier.PUBLIC;

    public static final int PRIVATE = Modifier.PRIVATE;

    public static final int PROTECTED = Modifier.PROTECTED;

    public static final int STATIC = Modifier.STATIC;

    public static final int FINAL = Modifier.FINAL;

    public static final int SYNCHRONIZED = Modifier.SYNCHRONIZED;

    public static final int VOLATILE = Modifier.VOLATILE;

    public static final int TRANSIENT = Modifier.TRANSIENT;

    public static final int NATIVE = Modifier.NATIVE;

    public static final int ABSTRACT = Modifier.ABSTRACT;

    public static final int STRICTFP = Modifier.STRICT;

    // https://docs.oracle.com/javase/7/docs/api/java/lang/reflect/Modifier.html
    // https://docs.oracle.com/javase/specs/jvms/se8/jvms8.pdf
    public static final int OPTIONAL = 0x08000;
    public static final int HARNESS =  0x10000;
    public static final int GENERATOR =  0x20000;
    // 0x40000 is taken by adt modifier in python part
    public static final int MODEL = 0x80000;

    public static AccessSpecifier getAccessSpecifier(int modifiers) {
        if (isPublic(modifiers)){
            return AccessSpecifier.PUBLIC;
        } else if (isProtected(modifiers)){
            return AccessSpecifier.PROTECTED;
        } else if (isPrivate(modifiers)){
            return AccessSpecifier.PRIVATE;
        } else {
            return AccessSpecifier.DEFAULT;
        }
    }

    public static int addModifier(int modifiers, int mod) {
        return modifiers | mod;
    }

    public static boolean hasModifier(int modifiers, int modifier) {
        return (modifiers & modifier) != 0;
    }

    public static boolean isAbstract(int modifiers) {
        return (modifiers & ABSTRACT) != 0;
    }

    public static boolean isFinal(int modifiers) {
        return (modifiers & FINAL) != 0;
    }

    public static boolean isNative(int modifiers) {
        return (modifiers & NATIVE) != 0;
    }

    public static boolean isPrivate(int modifiers) {
        return (modifiers & PRIVATE) != 0;
    }

    public static boolean isProtected(int modifiers) {
        return (modifiers & PROTECTED) != 0;
    }

    public static boolean isOptionals(int modifiers) {
        return (modifiers & OPTIONAL) != 0;
    }

    public static boolean isHarness(int modifiers) {
        return (modifiers & HARNESS) != 0;
    }

    public static boolean isGenerator(int modifiers) {
        return (modifiers & GENERATOR) != 0;
    }

    public static boolean isModel(int modifiers) {
        return (modifiers & MODEL) != 0;
    }
    
    /**
     * Is the element accessible from within the package?
     * It is the level of access which is applied if no modifiers are chosen,
     * it is sometimes called "default".
     * @param modifiers indicator
     * @return true if modifier denotes package level access
     */
    public static boolean hasPackageLevelAccess(int modifiers) {
        return !isPublic(modifiers) && !isProtected(modifiers) && !isPrivate(modifiers);
    }

    public static boolean isPublic(int modifiers) {
        return (modifiers & PUBLIC) != 0;
    }

    public static boolean isStatic(int modifiers) {
        return (modifiers & STATIC) != 0;
    }

    public static boolean isStrictfp(int modifiers) {
        return (modifiers & STRICTFP) != 0;
    }

    public static boolean isSynchronized(int modifiers) {
        return (modifiers & SYNCHRONIZED) != 0;
    }

    public static boolean isTransient(int modifiers) {
        return (modifiers & TRANSIENT) != 0;
    }

    public static boolean isVolatile(int modifiers) {
        return (modifiers & VOLATILE) != 0;
    }

    public static boolean isOptional(int modifiers) {
        return (modifiers & OPTIONAL) != 0;
    }

    /**
     * Removes the given modifier.
     * @param modifiers existing modifiers
     * @param mod modifier to be removed
     * @return result for removing modifier
     */
    public static int removeModifier(int modifiers, int mod) {
        return modifiers & ~mod;
    }

    private ModifierSet() {
    }
}
