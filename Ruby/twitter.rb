require 'twitter'

client = Twitter::REST::Client.new do |config|
	config.consumer_key = "xPA8KAyLtZexALgCNKLFedMHk"
	config.consumer_secret = "UIOdnTo5keXb4pYveBv2rF4fnKz4b6p7AV3gPqS0VNyBa94fTE"
	config.access_token = "930274637493293056-A557ABie8BxHK4YHChEQRLtrtkofVSO"
	config.access_token_secret = "a0rz2tREioB0g0F87OTK8znV4UnpkQ8vIOO1romknMKei"
end

client.update("Ruby is fun!")

puts "\nMy Friends: "
client.friends("mtirfan13").each {|f| puts f.name}

tweets = client.search("#XboxOne #PS4 -rt", lang: "en").take(10)
tweets.each do |tweet|
	puts "#{tweet.user.screen_name} -> #{tweet.text}"
end

require 'sqlite3'

twitterDB = SQLite3::Database.new("My Twitter Database")

twitterDB.execute("create table if not exists twitterTable (id INTEGER PRIMARY KEY, name TEXT, status TEXT);")
tweets.each_index do |i|
	rows = twitterDB.execute("select status from twitterTable where status = ?", tweets[i].text)
	if rows.length == 0
		twitterDB.execute("insert into twitterTable (name, status) values (?, ?)", tweets[i].user.screen_name, tweets[i].text)
	end
end

rows = twitterDB.execute("select name, status from twitterTable")
puts "Found #{rows.length} rows:"
rows.each do |row|
	puts row.join("-> ")
end