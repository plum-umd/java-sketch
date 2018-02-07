public class Tester {
    harness public void mn() {
	// File f = new File("#A\na;b;c;d;e;f;g;h;i;j\n");
	File f = new File("#A\na;b\n");

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
    }
}
