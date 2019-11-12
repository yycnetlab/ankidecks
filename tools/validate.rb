require 'optparse'
require 'json'

options = {}
OptionParser.new do |opts|
  opts.banner = "Usage: validate.rb [options]"

  opts.on("-f", "--file [FILE]", "File to validate") do |v|
    options[:file] = v
  end
end.parse!

if options[:file].nil? || !(File.exist?(options[:file]))
  STDERR.puts "File does not exist!"
  exit 1
end

def parse_file(file)
  file_contents = File.read(file)
  json_contents = nil

  begin
    json_contents = JSON.parse(file_contents)
  rescue
    STDERR.puts "Invalid JSON!"
    exit 1
  end

  json_contents
end

def check_duplicate_guids(notes)
  guids = notes.map { |note| note['guid']}
  if guids.uniq.length != guids.length
    puts "Duplicate GUID detected!"
    false
  else
    true
  end
end

def check_fields(notes)
  fields = ['Front', 'Back', 'Reverse ID', 'Reference']

  valid = true

  notes.each do |note|

    note['fields'].each_with_index do |item, index|
      if item == ""
        puts "Note with GUID #{note['guid']} has blank #{fields[index]}"
      end
    end

  end

  valid
end


json = parse_file(options[:file])
notes = json['notes']
valid = true


valid = valid && check_duplicate_guids(notes)
valid = valid && check_fields(notes)


if valid
  puts "Contents valid!"
else
  puts "Contents invalid!"
end