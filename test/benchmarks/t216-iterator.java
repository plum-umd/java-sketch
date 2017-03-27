class CharIterator implements Iterator<Character> {
    private final String str;
    private int pos = 0;

    public CharIterator(String str) {
        this.str = str;
    }

    public boolean hasNext() {
        return pos < str.length();
    }

    public Character next() {
        Character c = str.charAt(pos);
        pos = pos + 1;
        return c;
    }

    public void remove() {
        //throw new UnsupportedOperationException();
    }
}

class Test {
    harness static void test() {
        CharIterator cit = new CharIterator("hi");
        int i = 0;
        while (cit.hasNext()) {
            Character c = cit.next();
            if (i == 0) assert c == 'h';
            else if (i == 1) assert c == 'i';
            i = i + 1;
        }
    }
}

