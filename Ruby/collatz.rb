while true
	print "Input n > 0: "
	n = gets.chomp.to_i
	break if n > 0
end

puts "Input #{n} is #{n.class}"

out_file = File.new("collatz_#{n}.txt", "w")
if out_file
	out_file.write("#{n} -> ")
else
	raise "File error"
end
cycle_len = 0
while n != 1
	if n%2 ==0
		n /= 2
	else
		n = 3*n +1
	end
	out_file.write("#{n} ->")
	cycle_len += 1
end

puts "Cycle length = #{cycle_len}"

out_file.close
