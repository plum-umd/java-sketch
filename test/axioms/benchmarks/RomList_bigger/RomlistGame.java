package glog.frontend.attractmode;

public class RomlistGame {
	private String name;
	private String title;
	private String emulator;
	private String cloneOf;
	private String year;
	private String manufacturer;
	private String category;
	private String players;
	private String rotation;
	private String control;
	private String status;
	private String displayCount;
	private String displayType;
	private String altRomname;
	private String altTitle;
	private String extra;
	private String buttons;
	private boolean isAvailable;
	private boolean hasWheel;
	private boolean hasVideo;
	private boolean hasSnap;
	private boolean hasBox;
	private boolean hasCart;
	private boolean hasDatabase;
	/** Complete means having all games/wheels/video. */
	private boolean complete = true;
	private String romlist;
	private String fileName;
	private String wheelFileName;
	private String boxFileName;
	private String cartFileName;
	private String snapFileName;
	private String description;
	private String rating;
	private String releaseDate;
	private String developer;
	private String publisher;
	private String genre;
	private String pi3Status;
	private String pcStatus;
	private Long size = 0L;

	public String getName() {
		return name;
	}

	public void setName(String name) {
		this.name = name;
	}

	public String getTitle() {
		return title;
	}

	public void setTitle(String title) {
		this.title = title;
	}

	public String getEmulator() {
		return emulator;
	}

	public void setEmulator(String emulator) {
		this.emulator = emulator;
	}

	public String getCloneOf() {
		return cloneOf;
	}

	public void setCloneOf(String cloneOf) {
		this.cloneOf = cloneOf;
	}

	public String getYear() {
		return year;
	}

	public void setYear(String year) {
		this.year = year;
	}

	public String getManufacturer() {
		return manufacturer;
	}

	public void setManufacturer(String manufacturer) {
		this.manufacturer = manufacturer;
	}

	public String getCategory() {
		return category;
	}

	public void setCategory(String category) {
		this.category = category;
	}

	public String getPlayers() {
		return players;
	}

	public void setPlayers(String players) {
		this.players = players;
	}

	public String getRotation() {
		return rotation;
	}

	public void setRotation(String rotation) {
		this.rotation = rotation;
	}

	public String getControl() {
		return control;
	}

	public void setControl(String control) {
		this.control = control;
	}

	public String getStatus() {
		return status;
	}

	public void setStatus(String status) {
		this.status = status;
	}

	public String getDisplayCount() {
		return displayCount;
	}

	public void setDisplayCount(String displayCount) {
		this.displayCount = displayCount;
	}

	public String getDisplayType() {
		return displayType;
	}

	public void setDisplayType(String displayType) {
		this.displayType = displayType;
	}

	public String getAltRomname() {
		return altRomname;
	}

	public void setAltRomname(String altRomname) {
		this.altRomname = altRomname;
	}

	public String getAltTitle() {
		return altTitle;
	}

	public void setAltTitle(String altTitle) {
		this.altTitle = altTitle;
	}

	public String getExtra() {
		return extra;
	}

	public void setExtra(String extra) {
		this.extra = extra;
	}

	public String getButtons() {
		return buttons;
	}

	public void setButtons(String buttons) {
		this.buttons = buttons;
	}

	public boolean isAvailable() {
		return isAvailable;
	}

	public void setAvailable(boolean isAvailable) {
		this.isAvailable = isAvailable;
	}

	public boolean isHasWheel() {
		return hasWheel;
	}

	public void setHasWheel(boolean hasWheel) {
		this.hasWheel = hasWheel;
	}

	public boolean isHasVideo() {
		return hasVideo;
	}

	public void setHasVideo(boolean hasVideo) {
		this.hasVideo = hasVideo;
	}

	public boolean isComplete() {
		return complete;
	}

	public void setComplete(boolean complete) {
		this.complete = complete;
	}

	public String getRomlist() {
		return romlist;
	}

	public void setRomlist(String romlist) {
		this.romlist = romlist;
	}

	public String getFileName() {
		return fileName;
	}

	public void setFileName(String fileName) {
		this.fileName = fileName;
	}

	public String getWheelFileName() {
		return wheelFileName;
	}

	public void setWheelFileName(String wheelFileName) {
		this.wheelFileName = wheelFileName;
	}

	public String getSnapFileName() {
		return snapFileName;
	}

	public void setSnapFileName(String snapFileName) {
		this.snapFileName = snapFileName;
	}

	public boolean isHasDatabase() {
		return hasDatabase;
	}

	public void setHasDatabase(boolean hasDatabase) {
		this.hasDatabase = hasDatabase;
	}

	public String getDescription() {
		return description;
	}

	public void setDescription(String description) {
		this.description = description;
	}

	public boolean isHasBox() {
		return hasBox;
	}

	public void setHasBox(boolean hasBox) {
		this.hasBox = hasBox;
	}

	public boolean isHasCart() {
		return hasCart;
	}

	public void setHasCart(boolean hasCart) {
		this.hasCart = hasCart;
	}

	public String getBoxFileName() {
		return boxFileName;
	}

	public void setBoxFileName(String boxFileName) {
		this.boxFileName = boxFileName;
	}

	public String getCartFileName() {
		return cartFileName;
	}

	public void setCartFileName(String cartFileName) {
		this.cartFileName = cartFileName;
	}

	public String getRating() {
		return rating;
	}

	public void setRating(String rating) {
		this.rating = rating;
	}

	public String getReleaseDate() {
		return releaseDate;
	}

	public void setReleaseDate(String releaseDate) {
		this.releaseDate = releaseDate;
	}

	public String getDeveloper() {
		return developer;
	}

	public void setDeveloper(String developer) {
		this.developer = developer;
	}

	public String getPublisher() {
		return publisher;
	}

	public void setPublisher(String publisher) {
		this.publisher = publisher;
	}

	public String getGenre() {
		return genre;
	}

	public void setGenre(String genre) {
		this.genre = genre;
	}

	public String getPi3Status() {
		return pi3Status;
	}

	public void setPi3Status(String pi3Status) {
		this.pi3Status = pi3Status;
	}

	public String getPcStatus() {
		return pcStatus;
	}

	public void setPcStatus(String pcStatus) {
		this.pcStatus = pcStatus;
	}

	public Long getSize() {
		return size;
	}

	public void setSize(Long size) {
		this.size = size;
	}

	public boolean isHasSnap() {
		return hasSnap;
	}

	public void setHasSnap(boolean hasSnap) {
		this.hasSnap = hasSnap;
	}

}
