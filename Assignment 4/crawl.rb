load "open-uri.rb"
require "Addressable"

class WebCrawler
	@@verbose = false
	@@protocol = "http"
	@@visitedLinks = []
	@@brokenLinks = []
	@@allLinks = ["http://bowdoin.edu"]
	@@startURL = "http://bowdoin.edu"
	attr_reader :root

	def initialize(url)
		@root = url
	end

	def broken?(url)
		begin
			content = open(url).read
			broken = false
		rescue
			broken = true
		end
		broken
	end

	def getLinks(url, str)
		links = str.scan(/<a\s+href="(.+?)"/i).flatten
		#puts links
		#links.each do |oneLink|
			#oneLink.insert(0, url) if oneLink.start_with?("/")
		#end
	end

	def inDomain?(url, currURL)
		#if ( url =~ /.bowdoin.edu#{Regexp.escape("/")}catalogue/ )
		if ( url =~ /bowdoin.edu/ )
			true
		else
			#check for relative
			false
		end
	end

	# Note: very easy basic combination:
		# base = Addressable::URI.parse(currURL)
		# return base + link


	# split path into sections
	def getParts(link)
		path = URI(link).path
		if path
			parts = path.split("/")
			return parts
		end
	end

	# takes a relative link and a URL, returns an absolute link
	def makeAbsolute(link, currURL)
		if not ( link =~ /http/ )
			# relative link: create absolute link

			# .edu/pigs/index.html should be treated as .edu/pigs
			directory = /(.*.edu#{Regexp.escape("/")}).*\w+#{Regexp.escape(".")}.+$/.match(currURL)
			if directory
				currURL = directory[1]
			end

			# remove any trailing forward slash
			if currURL[-1] == "/"
				currURL = currURL[0..-2]
			end
			# if the link starts with "/", don't just append
			if ( link =~ /^#{Regexp.escape("/")}/ )
				domain = URI.parse(currURL).host
				link = "http://" + domain + link
				return link
			else
				# is ../ the start?
				if ( link =~ /^..#{Regexp.escape("/")}/ )
					# make sure you can actually go back a directory: look for bowdoin.edu/***/ at least
					if ( currURL =~ /.*bowdoin.edu#{Regexp.escape("/")}.*#{Regexp.escape("/")}?/ )
						# remove first instance of ../
						adjustedLink = link[3..-1]
						shortened = /.*#{Regexp.escape("/")}/.match(currURL)
						# remove / at end (guaranteed if the regex matches)
						shortened = shortened[0][0..-2]

						# another instance of ../?
						if ( adjustedLink =~ /^..#{Regexp.escape("/")}/ )
							# recurse on shortened URL
							result = makeAbsolute(adjustedLink, shortened)
						else
							result = shortened + "/" + adjustedLink
							return result
						end				
					end
				else
					# normal relative link - add to end

					currParts = getParts(currURL)
					linkParts = getParts(link)
					# lead to infinite repeats
					if currParts and linkParts
						if currParts[-1] == linkParts[0] or currParts[-1] == linkParts[0]
							puts "Repeats, avoiding " + link
							return currURL
						else
							return currURL + "/" + link
						end
					else
						return currURL
					end
				end
			end
		else
			# not relative
			return link
		end
	end

	def checkLinks(links, currURL)
		links.each do |link|
			link = makeAbsolute(link, currURL)
			if link and not link.length > 120
				# if site is in bowdoin.edu
				if inDomain?(link, currURL)
					# SPECIAL CASES:
					# leads to endless exploration (anchors)
					if ( link =~ /#{Regexp.escape("/")}#/ )
						@@brokenLinks.push(link)
						@@allLinks.push(link)
						next
					end
					# links nonresponsive, stall program
					if ( link =~ /academic.bowdoin/ )
						@@brokenLinks.push(link)
						@@allLinks.push(link)
						next
					end

					# if not already visited
					# MUCH more efficient would be a tree for lg n search & insert, based on directories
					if not @@visitedLinks.include? link
						# either add to broken or explore
						if broken?(link)
							if @@verbose
								puts "Link is broken " + link
							end
							# more efficient than looping through brokenLinks for every single link
							if not @@brokenLinks.include? link
								@@brokenLinks.push(link)
								@@allLinks.push(link)
							end
						else
							puts "Exploring " + link
							@@allLinks.push(link)
							@@visitedLinks.push(link)
							explore(link)
						end
					else
						if @@verbose
							puts "Already visited: " + link
						end
					end
				end
			end
		end
	end

	def explore(url)
		#while not @@allLinks.empty?
		if @@visitedLinks.length % 500 == 0
			puts "Hello, here is info:"
			results()
		end
			begin
				webPage = open(url).read
				links = getLinks(url, webPage)
				if @@verbose
					puts "********** Links **********\n"
					puts links
					puts "***************************\n\n"
				end	

				checkLinks(links, url)
			rescue
				puts "Error: "
				puts "\t#{$!}"
			end
		#end
	end

	def results()
		puts "***************************"
		puts "Explored #{@@visitedLinks.length} links, found #{@@brokenLinks.length} broken links."
		if @@verbose
			puts "Visited links:"
			puts @@visitedLinks
			puts "Broken links:"
			puts @@brokenLinks
		end
	end

end

url = "http://www.bowdoin.edu"

w = WebCrawler.new("http://www.bowdoin.edu")

w.explore(w.root)
w.results()

# question: more efficient to re-check broken links, or always check if in brokenLinks also? (probably the former, constant time)
