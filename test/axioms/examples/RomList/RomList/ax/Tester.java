public class Tester {
    harness public void mn() {
	File f = new File("#A\na;b;c;d;e;f;g;h;i;j");
	// File f = new File("#A\na;b\n");

	RomlistParser p = new RomlistParser();

	ArrayList<RomlistGame> games = p.parse(f);

	RomlistGame g1 = games.get(0);

	String name1 = g1.getName();
	String title1 = g1.getTitle();
	String emul1 = g1.getEmulator();
	String clone1 = g1.getCloneOf();
	String year1 = g1.getYear();
	String man1 = g1.getManufacturer();
	String cat1 = g1.getCategory();
	String plays1 = g1.getPlayers();
	String rot1 = g1.getRotation();
	String cont1 = g1.getControl();

	assert name1.equals("a");
	assert title1.equals("b");
	assert emul1.equals("c");
	assert clone1.equals("d");
	assert year1.equals("e");
	assert man1.equals("f");
	assert cat1.equals("g");
	assert plays1.equals("h");
	assert rot1.equals("i");
	assert cont1.equals("j");

	File f2 = new File("0;1;2;3;4;5;6;7;8;9\nq;w;e;r;t;y;u;i;o;p");
	// File f = new File("#A\na;b\n");

	RomlistParser p2 = new RomlistParser();

	ArrayList<RomlistGame> games2 = p2.parse(f2);

	RomlistGame g2 = games2.get(0);

	String name2 = g2.getName();
	String title2 = g2.getTitle();
	String emul2 = g2.getEmulator();
	String clone2 = g2.getCloneOf();
	String year2 = g2.getYear();
	String man2 = g2.getManufacturer();
	String cat2 = g2.getCategory();
	String plays2 = g2.getPlayers();
	String rot2 = g2.getRotation();
	String cont2 = g2.getControl();

	assert name2.equals("0");
	assert title2.equals("1");
	assert emul2.equals("2");
	assert clone2.equals("3");
	assert year2.equals("4");
	assert man2.equals("5");
	assert cat2.equals("6");
	assert plays2.equals("7");
	assert rot2.equals("8");
	assert cont2.equals("9");

	RomlistGame g3 = games2.get(1);

	String name3 = g3.getName();
	String title3 = g3.getTitle();
	String emul3 = g3.getEmulator();
	String clone3 = g3.getCloneOf();
	String year3 = g3.getYear();
	String man3 = g3.getManufacturer();
	String cat3 = g3.getCategory();
	String plays3 = g3.getPlayers();
	String rot3 = g3.getRotation();
	String cont3 = g3.getControl();

	assert name3.equals("q");
	assert title3.equals("w");
	assert emul3.equals("e");
	assert clone3.equals("r");
	assert year3.equals("t");
	assert man3.equals("y");
	assert cat3.equals("u");
	assert plays3.equals("i");
	assert rot3.equals("o");
	assert cont3.equals("p");	
    }
}
