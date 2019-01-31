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

    generator public void genRead(BufferedReader br, File romlistFile) {
	    String line = null;
	    if (??) {
		line = br.readLine();		
	    }
	    if (??) {
		while (line != null) {
		    genRead(br, romlistFile);
		}
	    }
	    if (??) {
		if (!line.startsWith("#")) {
			String[] data = line.split(";", -1);
			if (data.length >= 10) {
			// if (data.length >= 2) {
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
			     games.add(game);
			}
		}
	    }
	    if (??) {
		genRead(br, romlistFile);
	    }
	}

    generator BufferedReader genBufferedReader(int[] localInts, Object[] localObjs) {
	if (??) {
	    File f = (File) localObjs[0];
	    return new BufferedReader(f);
	}
	if (??) {
	    return localObjs[2];
	}
	return null;
    }
    
    generator RomListGame genRomListGame(int[] localInts, Object[] localObjs) {
	if (??) {
	    return new RomlistGame();
	}
	return null;
    }
    
    generator ArrayList<RomListGame> genArrayList(int[] localInts, Object[] localObjs) {
	if (??) {
	    return new ArrayList<RomListGame>();
	}
	if (??) {
	    return {| this.games, this.missingGames |};
	}
	return null;
    }
    
    generator String genString(int[] localInts, Object[] localObjs) {
	// if (??) {
	//     File f = (File) localObjs[0];
	//     return f.getName();
	// }
	if (??) {
	    BufferedReader br = (BufferedReader) localObjs[2];
	    return br.readLine();
	}
	// if (??) {
	//     Strings strs = genStrings(localInts, localObjs);
	//     String[] data = strs.toArray();
	//     return data[??];
	// }
	// if (??) {
	//     return localObjs[3];
	// }
	return null;
    }
    
    generator int genInt(int[] localInts, Object[] localObjs) {
	if (??) {
	    return this.games.size();
	}
	if (??) {
	    return this.missingGames.size();
	}
	if (??) {
	    Strings strs = (Strings) localObjs[4];
	    String[] data = strs.toArray();
	    return data.length;
	}
	if (??) {
	    return localInts[0];
	}
	return ??;
    }
    
    generator boolean guard(int[] localInts, Object[] localObjs) {
	boolean cond = false;
	if (??) {
	    File f = (File) localObjs[0];
	    cond = f.exists();
	}
	if (??) {
	    Object o1 = localObjs[0];
	    Object o2 = localObjs[1];
	    Object o3 = localObjs[2];
	    Object o4 = localObjs[3];
	    Object o5 = localObjs[4];
	    Object o6 = localObjs[5];
	    Object o = {| o1, o2, o3, o4, o5, o6 |};
	    cond = o == null;
	}
	if (??) {
	    String line = (String) localObjs[3];
	    cond = line.startsWith("#");
	}
	if (??) {
	    int i1 = genInt(localInts, localObjs);
	    int i2 = genInt(localInts, localObjs);
	    cond = {| i1 < i2, i1 <= i2, i1 == i2 |};
	}
	return {| cond, !cond |};
    }

    generator Strings genStrings(int[] localInts, Object[] localObjs) {
	if (??) {
	    String line = (String) localObjs[3];
	    return new Strings(line.split(";", -1));
	}
	return new Strings(new String[1]);
    }
    
    generator void voidFuncs(int[] localInts, Object[] localObjs) {
	// if (??) {
	//     String s = genString(localInts, localObjs);
	//     RomlistGame game = genRomListGame(localInts, localObjs);
	//     game.setRomlist(s);	    
	// }
	// if (??) {
	//     String s = genString(localInts, localObjs);
	//     RomlistGame game = genRomListGame(localInts, localObjs);
	//     game.setName(s);	    
	// }
	// if (??) {
	//     String s = genString(localInts, localObjs);
	//     RomlistGame game = genRomListGame(localInts, localObjs);
	//     game.setTitle(s);	    
	// }
	// if (??) {
	//     String s = genString(localInts, localObjs);
	//     RomlistGame game = genRomListGame(localInts, localObjs);
	//     game.setEmulator(s);	    
	// }
	// if (??) {
	//     String s = genString(localInts, localObjs);
	//     RomlistGame game = genRomListGame(localInts, localObjs);
	//     game.setCloneOf(s);	    
	// }
	// if (??) {
	//     String s = genString(localInts, localObjs);
	//     RomlistGame game = genRomListGame(localInts, localObjs);
	//     game.setYear(s);	    
	// }
	// if (??) {
	//     String s = genString(localInts, localObjs);
	//     RomlistGame game = genRomListGame(localInts, localObjs);
	//     game.setManufacturer(s);	    
	// }
	// if (??) {
	//     String s = genString(localInts, localObjs);
	//     RomlistGame game = genRomListGame(localInts, localObjs);
	//     game.setCategory(s);	    
	// }
	// if (??) {
	//     String s = genString(localInts, localObjs);
	//     RomlistGame game = genRomListGame(localInts, localObjs);
	//     game.setPlayers(s);	    
	// }
	// if (??) {
	//     String s = genString(localInts, localObjs);
	//     RomlistGame game = genRomListGame(localInts, localObjs);
	//     game.setRotation(s);	    
	// }
	// if (??) {
	//     String s = genString(localInts, localObjs);
	//     RomlistGame game = genRomListGame(localInts, localObjs);
	//     game.setControl(s);	    
	// }
	// if (??) {
	//     boolean b = guard(localInts, localObjs);
	//     RomlistGame game = genRomListGame(localInts, localObjs);
	//     game.setAvailable(b);	    	    
	// }
	if (??) {
	    RomlistGame game = genRomListGame(localInts, localObjs);
	    this.games.add(game);
	}
    }
    
    generator void stmts(int[] localInts, Object[] localObjs) {
	if (??) {
	    this.games = genArrayList(localInts, localObjs);
	}
	if (??) {
	    this.missingGames = genArrayList(localInts, localObjs);
	}
	if (??) {
	    localInts[0] = genInt(localInts, localObjs);
	}
	if (??) {
	    this.complete = guard(localInts, localObjs);
	}
	if (??) {
	    localObjs[2] = genBufferedReader(localInts, localObjs);
	}
	if (??) {
	    localObjs[3] = genString(localInts, localObjs);
	}
	if (??) {
	    localObjs[4] = genStrings(localInts, localObjs);
	}
	if (??) {
	    localObjs[5] = genRomListGame(localInts, localObjs);
	}
	if (??) {
	    this.totalGames = genInt(localInts, localObjs);
	}
	if (??) {
	    this.totalGamesAvailable = genInt(localInts, localObjs);
	}
	if (??) {
	    voidFuncs(localInts, localObjs);
	}
	// if (??) {
	//     stmts(localInts, localObjs);
	// }
    }
    
	/**
	 * @param romlistFile
	 * @param folderToSearch
	 * @return
	 * @throws Exception
	 */
	public ArrayList<RomlistGame> parse(File romlistFile, String folderToSearch, boolean lookAvailable) throws Exception {
	    Object[] localObjs = new Object[6];
	    localObjs[0] = romlistFile;
	    localObjs[1] = folderToSearch;
	    localObjs[3] = null;
	    int[] localInts = new int[1];

	    File f = (File) localObjs[0];

	    if (!f.exists()) {
	    	return new ArrayList<RomlistGame>();		
	    }

	    // if (guard(localInts, localObjs)) {
	    // 	return genArrayList(localInts, localObjs);
	    // }

	    // stmts(localInts, localObjs);
	    // stmts(localInts, localObjs);
	    // stmts(localInts, localObjs);
	    // stmts(localInts, localObjs);
	    // stmts(localInts, localObjs);
	    // stmts(localInts, localObjs);
	    
	    this.games = new ArrayList<RomListGame>();
	    this.missingGames = new ArrayList<RomListGame>();
	    localInts[0] = 0;
	    this.complete = true;

	    f = (File) localObjs[0];
	    localObjs[2] = new BufferedReader(f);

	    // BufferedReader br = (BufferedReader) localObjs[2];
	    // localObjs[3] = br.readLine();

	    stmts(localInts, localObjs);
	    BufferedReader br;
	    
	    while (localObjs[3] != null) {
	    	String line = (String) localObjs[3];
	    	if (!line.startsWith("#")) {
	    	    localObjs[4] = new Strings(line.split(";", -1));
		// if(guard(localInts, localObjs)) {
		//     stmts(localInts, localObjs);
	    	    Strings blah = (Strings) localObjs[4];
	    	    String[] data = blah.toArray();
		    if (data.length >= 10) {
		    // if (guard(localInts, localObjs)) {
			    localObjs[5] = new RomlistGame();			    
	    		    RomlistGame game = (RomlistGame) localObjs[5];
	    		    f = (File) localObjs[0];
	    		    game.setRomlist(f.getName());
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
	    		    // if (data.length > 10) {
	    		    // 	game.setStatus(data[10]);
	    		    // }
	    		    // if (data.length > 11) {
	    		    // 	game.setDisplayCount(data[11]);
	    		    // }
	    		    // if (data.length > 12) {
	    		    // 	game.setDisplayType(data[12]);
	    		    // }
	    		    // if (data.length > 13) {
	    		    // 	game.setAltRomname(data[13]);
	    		    // }
	    		    // if (data.length > 14) {
	    		    // 	game.setAltTitle(data[14]);
	    		    // }
	    		    // if (data.length > 15) {
	    		    // 	game.setExtra(data[15]);
	    		    // }
	    		    // if (data.length > 16) {
	    		    // 	game.setButtons(data[16]);
	    		    // }

	    		    game.setAvailable(false);
	    		    this.games.add(game);
			    // stmts(localInts, localObjs);
		    }
	    	}
	    	br = (BufferedReader) localObjs[2];
	    	localObjs[3] = br.readLine();
		// stmts(localInts, localObjs);
	    }

	    this.totalGames = this.games.size();
	    this.totalGamesAvailable = localInts[0];

	    return this.games;
	}

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

}
