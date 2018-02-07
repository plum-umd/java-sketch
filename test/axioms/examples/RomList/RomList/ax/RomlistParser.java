package glog.frontend.attractmode;

import java.io.BufferedReader;
import java.io.File;
import java.io.FileInputStream;
import java.io.FileReader;
import java.io.InputStream;
import java.io.InputStreamReader;
import java.nio.charset.Charset;
import java.nio.file.Files;
import java.nio.file.Paths;
import java.nio.file.StandardCopyOption;
import java.util.ArrayList;
import java.util.Arrays;
import java.util.Collections;
import java.util.Comparator;
import java.util.List;

import com.google.gson.Gson;

import glog.frontend.FrontendTools;
import glog.util.Util;

public class RomlistParser {
	private int totalGames;
	private int totalGamesAvailable;
	private int missingWheel;
	private int missingVideo;
	private int missingCart;
	private int missingBox;
	private ArrayList<RomlistGame> missingGames;
	private ArrayList<RomlistGame> games;
	private boolean complete;
	private String description;
	private String romPath;

	public RomlistParser() {
	    this.totalGames = 0;
	    this.totalGamesAvailable = 0;
	    this.missingWheel = 0;
	    this.missingVideo = 0;
	    this.missingCart = 0;
	    this.missingBox = 0;
	    this.missingGames = new ArrayList<>();
	    this.games = new ArrayList<>();
	    this.complete = false;
	    this.description = "";
	    this.romPath = "";
	}
    
	public ArrayList<RomlistGame> parse(File romlistFile) throws Exception {
		return parse(romlistFile, null);
	}

	public ArrayList<RomlistGame> parse(File romlistFile, String folderToSearch) throws Exception {
		return parse(romlistFile, folderToSearch, true);
	}

	/**
	 * @param romlistFile
	 * @param folderToSearch
	 * @return
	 * @throws Exception
	 */
	public ArrayList<RomlistGame> parse(File romlistFile, String folderToSearch, boolean lookAvailable) throws Exception {
		if (!romlistFile.exists()) {
			return new ArrayList<RomlistGame>();
		}
		String line;
		games = new ArrayList<RomlistGame>();
		missingGames = new ArrayList<RomlistGame>();
		int gamesAvailable = 0;
		this.complete = true;
		// try (InputStream fis = new FileInputStream(romlistFile); InputStreamReader isr = new InputStreamReader(fis, Charset.forName("UTF-8")); BufferedReader br = new BufferedReader(isr);) {
		// InputStream fis = new FileInputStream(romlistFile);
		// InputStreamReader isr = new InputStreamReader(fis, Charset.forName("UTF-8"));
		BufferedReader br = new BufferedReader(romlistFile);		
		line = br.readLine();
		while (line != null) {
			if (!line.startsWith("#")) {
			        String[] data = line.split(";", -1);
				if (data.length >= 10) {
				     RomlistGame game = new RomlistGame();
				     game.setRomlist(romlistFile.getName());
				     game.setName(data[0]);
				     game.setTitle(data[1]);
				     game.setEmulator(data[2]);
				     game.setCloneOf(data[3]);
				     game.setYear(data[4]);
				     game.setManufacturer(data[5]);
				     game.setCategory(data[6]);
				     game.setPlayers(data[7]);
				     game.setRotation(data[8]);
				     game.setControl(data[9]);
				     if (data.length > 10) {
					     game.setStatus(data[10]);
				     }
				     if (data.length > 11) {
					     game.setDisplayCount(data[11]);
				     }
				     if (data.length > 12) {
					     game.setDisplayType(data[12]);
				     }
				     if (data.length > 13) {
					     game.setAltRomname(data[13]);
				     }
				     if (data.length > 14) {
					     game.setAltTitle(data[14]);
				     }
				     if (data.length > 15) {
					     game.setExtra(data[15]);
				     }
				     if (data.length > 16) {
					     game.setButtons(data[16]);
				     }

				     game.setAvailable(false);
				     // if (lookAvailable) {
				     // 	EmulatorConfigFile ecf = new EmulatorConfigFile();
				     // 	if (!ecf.readConfig(data[2])) {
				     // 		System.out.println("WARNING!!!! Emulator config " + data[2] + " NOT FOUND! in " + romlistFile);
				     // 		continue;
				     // 	}

				     // 	if (this.checkGameAvailability(game, ecf, data, folderToSearch)) {
				     // 		this.romPath = ecf.getRompath();
				     // 		gamesAvailable++;
				     // 	}
				     // 	this.checkGameMediaAvailability(game, ecf, data);
				     // 	this.checkGameDatabaseAvailability(game, ecf, data);
				     // }

				     games.add(game);
				}
			}
			line = br.readLine();			
		}
		this.totalGames = games.size();
		this.totalGamesAvailable = gamesAvailable;

		// Check if there is metadata for the romlist.
		String a1 = romlistFile.getParent();
		String a2 = a1.concat("/database/");
		String a3 = a2.concat(romlistFile.getName());
		File nf = new File(a3);
		// if (nf.exists()) {
		// 	this.description = new String(Files.readAllBytes(Paths.get(romlistFile.getParent() + "/database/" + romlistFile.getName())));
		// }
		return games;
	}

	// private boolean checkGameAvailability(RomlistGame game, EmulatorConfigFile ecf, String[] data, String folderToSearch) {
	// 	// System.out.println("looking for " + game.getName() + " " + ecf.getRompath());
	// 	String[] exts = ecf.getRomext().split(";");
	// 	for (String ext : exts) {
	// 		File f = new File(ecf.getRompath() + "/" + data[0] + ext);
	// 		if (f.exists()) {
	// 			game.setAvailable(true);
	// 			game.setFileName(ecf.getRompath().replaceAll("\\\\", "/") + "/" + data[0] + ext);
	// 			game.setSize(f.length());
	// 			return true;
	// 		}
	// 	}
	// 	if (!game.isAvailable()) {
	// 		// Try different extensions not included in emulator.cfg files.
	// 		String[] altExts = { ".zip", ".7z", ".rar" };
	// 		for (String ext : altExts) {
	// 			File f = new File(ecf.getRompath() + "/" + data[0] + ext);
	// 			if (f.exists()) {
	// 				game.setAvailable(true);
	// 				game.setFileName(ecf.getRompath().replaceAll("\\\\", "/") + "/" + data[0] + ext);
	// 				game.setSize(f.length());
	// 				return true;
	// 			}
	// 		}
	// 		if (!game.isAvailable()) {
	// 			// Try folder name for CHDs...
	// 			File f = new File(ecf.getRompath() + "/" + data[0]);
	// 			if (f.exists() && f.isDirectory()) {
	// 				game.setAvailable(true);
	// 				game.setSize(Util.folderSize(f));
	// 				return true;
	// 			}
	// 			if (folderToSearch != null) {
	// 				for (String ext : exts) {
	// 					System.out.println("Checking " + folderToSearch + "/" + game.getEmulator() + "/roms/" + data[0] + ext);
	// 					f = new File(folderToSearch + "/" + game.getEmulator() + "/roms/" + data[0] + ext);
	// 					if (f.exists()) {
	// 						game.setAvailable(true);
	// 						game.setFileName(folderToSearch + "/" + game.getEmulator() + "/roms/" + data[0] + ext);
	// 						game.setSize(f.length());
	// 						return true;
	// 					}
	// 				}
	// 				if (!game.isAvailable()) {
	// 					// Try folder name for CHDs...
	// 					f = new File(folderToSearch + "/" + game.getEmulator() + "/roms/" + data[0]);
	// 					if (f.exists() && f.isDirectory()) {
	// 						game.setAvailable(true);
	// 						game.setSize(Util.folderSize(f));
	// 						return true;
	// 					}
	// 				}
	// 			}
	// 		}

	// 		if (!game.isAvailable()) {
	// 			this.missingGames.add(game);
	// 		}
	// 	}
	// 	return false;

	// }

	// private void checkGameMediaAvailability(RomlistGame game, EmulatorConfigFile ecf, String[] data) throws Exception {
	// 	boolean wheel = new File(ecf.getWheelPath() + "/" + data[0] + ".png").exists() || new File(ecf.getWheelPath() + "/" + data[0] + ".jpg").exists();
	// 	if (!wheel) {
	// 		missingWheel++;
	// 	} else {
	// 		if (new File(ecf.getWheelPath() + "/" + data[0] + ".png").exists()) {
	// 			game.setWheelFileName(ecf.getWheelPath() + "/" + data[0] + ".png");
	// 		}
	// 	}
	// 	game.setHasWheel(wheel);

	// 	boolean cart = new File(ecf.getCartPath() + "/" + data[0] + ".png").exists() || new File(ecf.getCartPath() + "/" + data[0] + ".jpg").exists();
	// 	if (!cart) {
	// 		missingCart++;
	// 	} else {
	// 		if (new File(ecf.getCartPath() + "/" + data[0] + ".png").exists()) {
	// 			game.setCartFileName(ecf.getCartPath() + "/" + data[0] + ".png");
	// 		}
	// 	}
	// 	game.setHasCart(cart);

	// 	boolean box = new File(ecf.getBoxPath() + "/" + data[0] + ".png").exists() || new File(ecf.getBoxPath() + "/" + data[0] + ".jpg").exists();
	// 	if (!box) {
	// 		missingBox++;
	// 	} else {
	// 		if (new File(ecf.getBoxPath() + "/" + data[0] + ".png").exists()) {
	// 			game.setBoxFileName(ecf.getBoxPath() + "/" + data[0] + ".png");
	// 		}
	// 	}
	// 	game.setHasBox(box);

	// 	boolean video = new File(ecf.getSnapPath() + "/" + data[0] + ".mp4").exists() || new File(ecf.getSnapPath() + "/" + data[0] + ".png").exists() || new File(ecf.getWheelPath() + "/" + data[0] + ".jpg").exists();
	// 	if (!video) {
	// 		missingVideo++;
	// 	} else {
	// 		if (new File(ecf.getSnapPath() + "/" + data[0] + ".mp4").exists()) {
	// 			game.setSnapFileName(ecf.getSnapPath() + "/" + data[0] + ".mp4");
	// 		}
	// 	}
	// 	game.setHasVideo(video);
	// 	if (!game.isAvailable() || !game.isHasVideo() || !game.isHasWheel()) {
	// 		game.setComplete(false);
	// 		this.complete = false;
	// 	}
	// }

	// private void checkGameDatabaseAvailability(RomlistGame game, EmulatorConfigFile ecf, String[] data) throws Exception {
	// 	File db = new File(ecf.getRompath() + "/database/" + data[0] + ".json");
	// 	game.setHasDatabase(db.exists());
	// 	if (db.exists()) {
	// 		Gson gson = new Gson();
	// 		RomlistGame tmp = gson.fromJson(new FileReader(ecf.getRompath() + "/database/" + game.getName() + ".json"), RomlistGame.class);
	// 		game.setPcStatus(tmp.getPcStatus());
	// 		game.setPi3Status(tmp.getPi3Status());
	// 		game.setDescription(tmp.getDescription());
	// 	}
	// }

	public boolean isComplete() {
		return complete;
	}

	public void setComplete(boolean complete) {
		this.complete = complete;
	}

	public int getTotalGames() {
		return totalGames;
	}

	public void setTotalGames(int totalGames) {
		this.totalGames = totalGames;
	}

	public int getTotalGamesAvailable() {
		return totalGamesAvailable;
	}

	public void setTotalGamesAvailable(int totalGamesAvailable) {
		this.totalGamesAvailable = totalGamesAvailable;
	}

	public int getMissingWheel() {
		return missingWheel;
	}

	public ArrayList<RomlistGame> getGames() {
		return games;
	}

	public void setMissingWheel(int missingWheel) {
		this.missingWheel = missingWheel;
	}

	public int getMissingVideo() {
		return missingVideo;
	}

	public int getMissingCart() {
		return missingCart;
	}

	public int getMissingBox() {
		return missingBox;
	}

	public void setMissingVideo(int missingVideo) {
		this.missingVideo = missingVideo;
	}

	public ArrayList<RomlistGame> getMissingGames() {
		return missingGames;
	}

	public void setMissingGames(ArrayList<RomlistGame> missingGames) {
		this.missingGames = missingGames;
	}

	// public void generateEmptyRomFiles(String romlistFile, String destFolder) throws Exception {
	// 	for (RomlistGame game : parse(new File(romlistFile))) {
	// 		new File(destFolder + "/" + game.getName() + ".zip").createNewFile();
	// 	}
	// }

	// public void generateRetroarchConfFileAllGames(String romlistFile, String destFolder) throws Exception {
	// 	for (RomlistGame game : parse(new File(romlistFile))) {
	// 		String msg = "input_overlay_enable = false\naspect_ratio_index = \"21\"";
	// 		Files.write(Paths.get(destFolder + game.getName() + ".cfg"), msg.getBytes());
	// 	}
	// }

	// public void generateRetroarchConfFileAllGames(File folder, String destFolder) throws Exception {
	// 	for (String rom : folder.list()) {
	// 		if (!new File(destFolder + " " + rom + ".cfg").exists()) {
	// 			String msg = "input_overlay_enable = false\naspect_ratio_index = \"21\"";
	// 			Files.write(Paths.get(destFolder + rom.replaceAll(".zip", "") + ".cfg"), msg.getBytes());
	// 		}
	// 	}
	// }

	// /**
	//  * Method to search for arcade roms in FBA, and MAME romsets.
	//  * 
	//  * mame4all = "/opt/retropie/emulators/mame4all/mame %BASENAME%"
	//  * 
	//  * pifba = "/opt/retropie/emulators/pifba/fba2x %ROM%"
	//  * 
	//  * lr-fbalpha = "/opt/retropie/emulators/retroarch/bin/retroarch -L /opt/retropie/libretrocores/lr-fbalpha/fbalpha_libretro.so --config /opt/retropie/configs/arcade/retroarch.cfg %ROM%"
	//  * 
	//  * lr-imame4all = "/opt/retropie/emulators/retroarch/bin/retroarch -L /opt/retropie/libretrocores/lr-imame4all/mame2000_libretro.so --config /opt/retropie/configs/arcade/retroarch.cfg %ROM%"
	//  * 
	//  * lr-mame2003 = "/opt/retropie/emulators/retroarch/bin/retroarch -L /opt/retropie/libretrocores/lr-mame2003/mame2003_libretro.so --config /opt/retropie/configs/arcade/retroarch.cfg %ROM%"
	//  * 
	//  * advmame-0.94.0 = "/opt/retropie/emulators/advmame/0.94.0/bin/advmame %BASENAME%"
	//  * 
	//  * advmame-1.4 = "/opt/retropie/emulators/advmame/1.4/bin/advmame %BASENAME%"
	//  * 
	//  * lr-mame2010 = "/opt/retropie/emulators/retroarch/bin/retroarch -L /opt/retropie/libretrocores/lr-mame2010/mame2010_libretro.so --config /opt/retropie/configs/arcade/retroarch.cfg %ROM%"
	//  * 
	//  * lr-fbalpha2012 = "/opt/retropie/emulators/retroarch/bin/retroarch -L /opt/retropie/libretrocores/lr-fbalpha2012/fbalpha2012_libretro.so --config /opt/retropie/configs/arcade/retroarch.cfg %ROM%"
	//  * 
	//  * advmame-3.1 = "/opt/retropie/emulators/advmame/3.1/bin/advmame %BASENAME%"
	//  * 
	//  * @param romlistFile
	//  * @throws Exception
	//  */
	// public void findMissingArcadeRoms(String romlistFile, boolean copy) throws Exception {
	// 	for (RomlistGame game : parse(new File(romlistFile))) {
	// 		boolean found = false;
	// 		String emulator = game.getEmulator();
	// 		if (!game.isAvailable()) {
	// 			if (new File("G:/roms/FB Alpha 0.2.97.38 Non-Merged/FB Alpha 0.2.97.38/roms/" + game.getName() + ".zip").exists()) {
	// 				// System.out.println(game.getName() + " FBA 0.2.97.38");
	// 				if (copy) {
	// 					Util.copyFile("G:/roms/FB Alpha 0.2.97.38 Non-Merged/FB Alpha 0.2.97.38/roms/" + game.getName() + ".zip", "c:/temp/missing/" + game.getName() + ".zip", false);
	// 				}
	// 				found = true;
	// 				emulator = "lr-fbalpha";
	// 			}
	// 			if (new File("G:/roms/MAME 0.139u1 ROMs/" + game.getName() + ".zip").exists()) {
	// 				// System.out.println(game.getName() + " MAME 0.139");
	// 				if (copy) {
	// 					Util.copyFile("G:/roms/MAME 0.139u1 ROMs/" + game.getName() + ".zip", "c:/temp/missing/" + game.getName() + ".zip", false);
	// 				}
	// 				found = true;
	// 				emulator = "lr-mame2010";
	// 			}
	// 			if (new File("G:/roms/mame78/" + game.getName() + ".zip").exists()) {
	// 				// System.out.println(game.getName() + " MAME 0.78");
	// 				if (copy) {
	// 					Util.copyFile("G:/roms/mame78/" + game.getName() + ".zip", "c:/temp/missing/" + game.getName() + ".zip", false);
	// 				}
	// 				found = true;
	// 				emulator = "lr-mame2003";
	// 			}
	// 			if (new File("G:/roms/mame-mame4all/" + game.getName() + ".zip").exists()) {
	// 				// System.out.println(game.getName() + " MAME4ALL");
	// 				if (copy) {
	// 					Util.copyFile("G:/roms/mame-mame4all/" + game.getName() + ".zip", "c:/temp/missing/" + game.getName() + ".zip", false);
	// 				}
	// 				found = true;
	// 				emulator = "lr-mame2003";
	// 			}
	// 			// System.out.println(game.getName() + " NOT FOUND!");
	// 		} else {
	// 			found = true;
	// 		}
	// 		if (found) {
	// 			if (game.isHasWheel() && game.isHasVideo()) {
	// 				System.out.println(game.getName() + ";" + game.getTitle() + ";" + emulator + ";;" + game.getYear() + ";" + game.getManufacturer() + ";" + game.getCategory() + ";;;;;0;;;;;");
	// 			}
	// 			if (copy) {
	// 				FrontendTools.findMediaForRomByName(game.getName(), "g:/glog/platform/mame/media/wheel/classic/", ".png", "C:/emulators/arcadepi/roms/arcade/wheel/", false);
	// 				FrontendTools.findMediaForRomByName(game.getName(), "g:/glog/platform/mame/media/video/", ".mp4", "C:/emulators/arcadepi/roms/arcade/snap/", false);
	// 			}
	// 		}
	// 	}
	// }

	// public void showMissingGames(String romlistFile) throws Exception {
	// 	for (RomlistGame game : parse(new File(romlistFile))) {
	// 		if (!game.isAvailable()) {
	// 			System.out.println(game.getName() + " " + game.getTitle() + " " + game.getEmulator());
	// 		}
	// 	}
	// }

	// public void showMissingWheels(String romlistFile) throws Exception {
	// 	for (RomlistGame game : parse(new File(romlistFile))) {
	// 		if (!game.isHasWheel()) {
	// 			System.out.println(game.getName() + " " + game.getTitle() + " " + game.getEmulator());
	// 		}
	// 	}
	// }

	// public void showMissingCarts(String romlistFile) throws Exception {
	// 	for (RomlistGame game : parse(new File(romlistFile))) {
	// 		if (!game.isHasCart()) {
	// 			System.out.println(game.getName() + " " + game.getTitle() + " " + game.getEmulator());
	// 		}
	// 	}
	// }

	// public void showMissingVideos(String romlistFile) throws Exception {
	// 	for (RomlistGame game : parse(new File(romlistFile))) {
	// 		if (!game.isHasVideo()) {
	// 			System.out.println(game.getName() + " " + game.getTitle() + " " + game.getEmulator());
	// 		}
	// 	}
	// }

	// public void showMissingBoxes(String romlistFile) throws Exception {
	// 	for (RomlistGame game : parse(new File(romlistFile))) {
	// 		if (!game.isHasBox()) {
	// 			System.out.println(game.getName() + " " + game.getTitle() + " " + game.getEmulator());
	// 		}
	// 	}
	// }

	// public void removeMedia() throws Exception {
	// 	String[] roms = new File("C:/emulators/arcadepi/roms/arcade/snap").list();
	// 	String[] romlists = new File("C:/attract-v2.2.0-1-win64/romlists/").list();
	// 	List<String> names = new ArrayList<String>();
	// 	for (String romlist : romlists) {
	// 		if (romlist.endsWith(".txt")) {
	// 			for (RomlistGame game : parse(new File("C:/attract-v2.2.0-1-win64/romlists/" + romlist))) {
	// 				names.add(game.getName() + ".mp4");
	// 			}
	// 		}
	// 	}
	// 	for (String rom : roms) {
	// 		if (!names.contains(rom)) {
	// 			System.out.println(rom);
	// 			new File("C:/emulators/arcadepi/roms/arcade/snap/" + rom).delete();
	// 			// Util.copyFile("C:/emulators/arcadepi/roms/arcade/snap/" + rom, "c:/temp/missing/video/" + rom, false);
	// 		}
	// 	}
	// }

	// public void printRomlistInAlphabeticalOrder(String romlistFile) throws Exception {
	// 	List<RomlistGame> games = parse(new File(romlistFile));
	// 	Collections.sort(games, new Comparator<RomlistGame>() {
	// 		@Override
	// 		public int compare(final RomlistGame object1, final RomlistGame object2) {
	// 			return object1.getName().compareTo(object2.getName());
	// 		}
	// 	});
	// 	for (RomlistGame game : games) {
	// 		System.out.println(game.getName() + ";" + game.getTitle() + ";" + game.getEmulator() + ";;" + game.getYear() + ";" + game.getManufacturer() + ";" + game.getCategory() + ";;;;;0;;;;;");
	// 	}
	// }

	// public boolean findGame(String name) {
	// 	for (RomlistGame g : games) {
	// 		if (g.getName().startsWith(name)) {
	// 			return true;
	// 		}
	// 	}
	// 	return false;
	// }

	// public void createRomlistBasedOnFolder(String romFolder, String emulator) throws Exception {
	// 	String[] files = new File(romFolder).list();
	// 	Arrays.sort(files);
	// 	for (String file : files) {
	// 		if (!new File(romFolder + file).isDirectory()) {
	// 			String name = file.substring(0, file.lastIndexOf("."));
	// 			System.out.println(name + ";" + name + ";" + emulator + ";;;;;;;;;;;;0;;;;;");
	// 		}
	// 	}
	// }

	// /**
	//  * Mostly used for arcade games that have several options of emulators to launch a game.
	//  * 
	//  * @param prefix
	//  * @param romlistFile
	//  * @throws Exception
	//  */
	// public void createEmulatorsConfigFileForRetropie(String prefix, String romlistFile) throws Exception {
	// 	List<RomlistGame> games = parse(new File(romlistFile));
	// 	for (RomlistGame game : games) {
	// 		System.out.println(prefix + "_" + game.getName() + " = \"" + game.getEmulator() + "\"");
	// 	}
	// }

	// public RomlistGame getGameByName(String gameName) {
	// 	for (RomlistGame game : games) {
	// 		if (game.getName().equals(gameName)) {
	// 			return game;
	// 		}
	// 	}
	// 	return null;
	// }

	// public String getDescription() {
	// 	return description;
	// }

	// public void setDescription(String description) {
	// 	this.description = description;
	// }

	// public void separateRoms() throws Exception {
	// 	String[] romlists = new File("C:/Temp/romlists/").list();
	// 	for (String romlist : romlists) {
	// 		File f = new File("C:/Temp/romlists/" + romlist);
	// 		if (f.isFile() && f.getName().endsWith(".txt")) {
	// 			RomlistParser rp = new RomlistParser();
	// 			rp.parse(f);
	// 			System.out.println(romlist + " " + rp.getGames().size());
	// 			for (RomlistGame g : rp.getGames()) {
	// 				if ("lr-mame2010".equals(g.getEmulator())) {
	// 					if (g.getFileName() != null) {
	// 						// System.out.println(g.getFileName() + " " + );
	// 						File source = new File(g.getFileName());
	// 						File dest = new File("c:/emulators/arcade/mame2010/" + g.getFileName().substring(g.getFileName().lastIndexOf("/") + 1));
	// 						if (!dest.exists()) {
	// 							Files.copy(source.toPath(), dest.toPath());
	// 						}
	// 					}
	// 				}
	// 			}
	// 		}
	// 	}
	// }

	// private void temp() throws Exception {
	// 	String[] roms = new File("C:/emulators/arcade/fbalpha").list();
	// 	for (String rom : roms) {
	// 		rom = rom.replace(".zip", "");
	// 		File db = new File("C:/emulators/arcadepi/roms/arcade/database/" + rom + ".json");
	// 		if (db.exists()) {
	// 			if (!new File("c:/emulators/arcade/fbalpha/database/" + rom + ".json").exists()) {
	// 				Files.copy(db.toPath(), new File("c:/emulators/arcade/fbalpha/database/" + rom + ".json").toPath());
	// 			}
	// 		}
	// 	}

	// }

	// private void temp2() throws Exception {
	// 	RomlistParser rp = new RomlistParser();
	// 	rp.parse(new File("c:/attract-v2.2.0-1-win64/romlists/Yun Sung.txt"));
	// 	for (RomlistGame g : rp.getMissingGames()) {
	// 		String emu = g.getEmulator().replaceAll("lr-", "");
	// 		File source = new File("c:/emulators/arcade/mame2003/" + g.getName() + ".zip");
	// 		File target = new File("c:/emulators/arcade/" + emu + "/" + g.getName() + ".zip");
	// 		if (source.exists()) {
	// 			Files.move(source.toPath(), target.toPath(), StandardCopyOption.REPLACE_EXISTING);
	// 		} else {
	// 			source = new File("c:/emulators/arcade/mame2010/" + g.getName() + ".zip");
	// 			if (source.exists()) {
	// 				Files.move(source.toPath(), target.toPath(), StandardCopyOption.REPLACE_EXISTING);
	// 			} else {
	// 				source = new File("c:/emulators/arcade/fbalpha/" + g.getName() + ".zip");
	// 				if (source.exists()) {
	// 					Files.move(source.toPath(), target.toPath(), StandardCopyOption.REPLACE_EXISTING);
	// 				}
	// 			}
	// 		}
	// 		// System.out.println(g.getName() + " " + g.getFileName());
	// 	}

	// }

	// private String findRom(String name) throws Exception {
	// 	File source = new File("c:/emulators/arcade/mame2003/" + name + ".zip");
	// 	if (source.exists()) {
	// 		return "lr-mame2003";
	// 	} else {
	// 		source = new File("c:/emulators/arcade/mame2010/" + name + ".zip");
	// 		if (source.exists()) {
	// 			return "lr-mame2010";
	// 		} else {
	// 			source = new File("c:/emulators/arcade/fbalpha/" + name + ".zip");
	// 			if (source.exists()) {
	// 				return "lr-fbalpha";
	// 			}
	// 		}
	// 	}

	// 	source = new File("G:/roms/mame78/" + name + ".zip");
	// 	File target = new File("c:/emulators/arcade/mame2003/" + name + ".zip");
	// 	if (source.exists()) {
	// 		Files.copy(source.toPath(), target.toPath());
	// 		return "lr-mame2003";
	// 	} else {
	// 		source = new File("G:/roms/MAME 0.139u1 ROMs/" + name + ".zip");
	// 		target = new File("c:/emulators/arcade/mame2010/" + name + ".zip");
	// 		if (source.exists()) {
	// 			Files.copy(source.toPath(), target.toPath());
	// 			return "lr-mame2010";
	// 		}
	// 	}

	// 	return "lr-mame2003";
	// }

	// private void adjustRomlist() throws Exception {
	// 	RomlistParser rp = new RomlistParser();
	// 	rp.parse(new File("c:/attract-v2.2.0-1-win64/romlists/Beatemup Arcade.txt"));
	// 	for (RomlistGame g : rp.getGames()) {
	// 		String emulator = g.getEmulator();
	// 		if (!g.isAvailable()) {
	// 			emulator = findRom(g.getName());
	// 		}
	// 		System.out.println(g.getName() + ";" + g.getTitle() + ";" + emulator + ";;;;;;;;;;;;0;;;;;");
	// 	}
	// }

	// public String getRomPath() {
	// 	return romPath;
	// }

	// public static void main(String[] args) throws Exception {
	// 	RomlistParser p = new RomlistParser();

	// 	// p.separateRoms();
	// 	// p.temp();
	// 	p.adjustRomlist();
	// 	System.exit(0);

	// 	// p.generateRetroarchConfFileAllGames("C:/attract-v2.2.0-1-win64/romlists/Arcade.txt", "c:/temp/retrocfg/");
	// 	p.generateRetroarchConfFileAllGames(new File("c:/emulators/arcade/fbalpha"), "c:/temp/retrocfg/");
	// 	System.exit(0);

	// 	// p.createEmulatorsConfigFileForRetropie("arcade", "C:/attract-v2.2.0-1-win64/romlists/lfe-all-retropie-pi-systems-full/Arcade.txt");
	// 	// System.exit(0);

	// 	p.createRomlistBasedOnFolder("C:/emulators/Cave 3rd/roms", "Cave 3rd");
	// 	// System.exit(0);
	// 	// p.showMissingWheels("C:/attract-v2.2.0-1-win64/romlists/Atari 2600.txt");
	// 	// System.exit(0);

	// 	// p.showMissingGames("C:/attract-v2.2.0-1-win64/romlists/Batman Collection.txt");
	// 	// System.exit(0);

	// 	// p.generateEmptyRomFiles("C:/attract-v2.2.0-1-win64/romlists/Acorn Electron.txt", "c:/temp/tmp/");
	// 	// System.exit(0);

	// 	// p.showMissingVideos("C:/attract-v2.2.0-1-win64/romlists/007 Collection.txt");
	// 	System.exit(0);

	// 	// p.findMissingArcadeRoms("C:/attract-v2.2.0-1-win64/romlists/Baseball Collection.txt", false);
	// 	// p.showMissingVideos("C:/attract-v2.2.0-1-win64/romlists/Arcade.txt");
	// 	// p.removeMedia();
	// 	// System.exit(0);

	// 	// p.generateEmptyRomFiles("C:/attract-v2.2.0-1-win64/romlists/Tandy TRS-80 Color Computer.txt", "c:/temp/tandy");
	// 	// System.exit(0);

	// 	for (RomlistGame game : p.parse(new File("C:/attract-v2.2.0-1-win64/romlists/007 Collection.txt"))) {
	// 		System.out.println(game.getFileName() + " -> " + game.getEmulator());
	// 	}
	// 	System.exit(0);

	// 	for (RomlistGame game : p.parse(new File("C:/attract-v2.2.0-1-win64/romlists/temp/Commodore 64.txt"))) {
	// 		if (!game.isAvailable() || !game.isHasWheel() || !game.isHasVideo()) {
	// 			// System.out.println(game.getName() + " " + game.getEmulator());
	// 			EmulatorConfigFile ecf = new EmulatorConfigFile();
	// 			ecf.readConfig(game.getEmulator());

	// 			Util.copyFile("g:/glog/platform/" + game.getEmulator() + "/roms/" + game.getName() + ".zip", ecf.getRompath() + "/" + game.getName() + ".zip", false);
	// 			FrontendTools.findMediaForRomByName(game.getName(), "g:/glog/platform/" + game.getEmulator() + "/media/wheel/classic/", ".png", ecf.getRompath() + "/wheel/", false);
	// 			FrontendTools.findMediaForRomByName(game.getName(), "g:/glog/platform/" + game.getEmulator() + "/media/video/", ".mp4", ecf.getSnapPath() + "/", false);

	// 			// Util.copyFile("G:/roms/FB Alpha 0.2.97.38 Non-Merged/FB Alpha 0.2.97.38/roms/" + game.getName() + ".zip", ecf.getRompath() + "/" + game.getName() + ".zip", false);
	// 			// FrontendTools.findMediaForRomByName(game.getName(), "g:/glog/platform/mame/media/wheel/classic/", ".png", ecf.getRompath() + "/wheel/", false);
	// 			// FrontendTools.findMediaForRomByName(game.getName(), "g:/glog/platform/mame/media/video/", ".mp4", ecf.getSnapPath() + "/", false);

	// 		}

	// 	}
	// }

}
