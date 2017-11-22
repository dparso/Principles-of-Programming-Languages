load "open-uri.rb"

def getLinks(url, str)
	links = str.scan(/<a\s+href="(.+?)"/i).flatten
	links.each do |oneLink|
		oneLink.insert(0, url) if oneLink.start_with?("/")
	end
end

url = "http://www.bowdoin.edu"

begin
	webPage = open(url).read
	links = getLinks(url, webPage)
	puts links
	puts "# of links = #{links.size}"
rescue
	puts "Error: "
	puts "\t#{$!}"
end
puts "\nEnd of file"