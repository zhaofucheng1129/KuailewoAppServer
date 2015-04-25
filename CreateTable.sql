/*搞笑图片*/
create table a_amusing_img(
	item_id int auto_increment primary key,
	title varchar(1000),
	source varchar(100),
	source_url varchar(1000),
	img_url varchar(1000),
	up_vote int,
	down_vote int,
	create_time varchar(20),
	release_time varchar(20),
	tags varchar(500),
	width int,
	height int,
	format varchar(20)
);
/*美女图片*/
create table a_amusing_beauty(
	item_id int auto_increment primary key, 
	title varchar(1000),
	source varchar(100),
	source_url varchar(1000),
	img_url varchar(1000),
	up_vote int,
	down_vote int,
	create_time varchar(20),
	width int,
	height int,
	format varchar(20)
);
/*声音专辑*/
create table a_amusing_album(
	album_id varchar(20) primary key,
	album_title varchar(1000),
	album_source varchar(100),
	album_url varchar(1000),
	album_img varchar(1000),
	album_play_count int,
	tag_list varchar(1000),
	sound_count int,
	category_name varchar(500),
	category_title varchar(500),
	create_time varchar(20),
	update_time varchar(20)
);
/*声音*/
create table a_amusing_audio(
	id varchar(20) primary key,
	album_id varchar(20),
	album_title varchar(1000),
	category_name varchar(500),
	category_title varchar(500),
	comments_count int,
	cover_url varchar(1000),
	cover_url_142 varchar(1000),
	duration float(15,3),
	favorites_count int,
	formatted_created_at varchar(100),
	have_more_intro varchar(100),
	intro varchar(5000),
	is_favorited varchar(100),
	nickname varchar(500),
	play_count int,
	play_path varchar(1000),
	play_path_32 varchar(1000),
	play_path_64 varchar(1000),
	play_path_128 varchar(1000),
	played_secs varchar(100),
	shares_count int,
	short_intro varchar(1000),
	time_until_now varchar(100),
	title varchar(1000),
	uid varchar(100),
	in_albums varchar(500),
	create_time varchar(20),
	update_time varchar(20)
)