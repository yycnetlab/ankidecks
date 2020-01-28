require 'optparse'
require 'json'

options = {
    config: 'config.json'
}
OptionParser.new do |opts|
  opts.banner = "Usage: add_note.rb [options]"

  opts.on("-f", "--file [FILE]", "File to modify") do |v|
    options[:file] = v
  end

  opts.on("-n", "--note [FILE]", "Note JSON to add") do |v|
    options[:note] = v
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
    STDERR.puts "Invalid JSON in file #{file}!"
    exit 1
  end

  json_contents
end

#Deep copy is unnecessary
def get_last_guid(file_json)
  file_json['notes'].last['guid'].dup
end

# Trim the prefix off of the last GUID, increment, then prepend a new prefix.
def get_next_guids(prefix, last_guid)
  length = last_guid.length - prefix.length
  last_guid = last_guid[prefix.length..-1].to_i

  res1 = (last_guid + 1).to_s.rjust(length, '0').prepend(prefix);
  res2 = (last_guid + 2).to_s.rjust(length, '0').prepend(prefix);

  return res1, res2
end

file_json = parse_file(options[:file])
note_json = parse_file(options[:note])
config_json = parse_file(options[:config])

note_data = file_json['notes'][0]

last_guid = get_last_guid(file_json)
first_guid, second_guid = get_next_guids(config_json['prefix'], last_guid)

# Deep copy template
front_card = Marshal.load(Marshal.dump(note_data))
reverse_card = Marshal.load(Marshal.dump(note_data))

front_card["fields"][0] = note_json["front"]
front_card["fields"][1] = note_json["back"]
front_card["fields"][2] = second_guid
front_card["fields"][3] =  note_json["reference"]
front_card["guid"]      =  first_guid

reverse_card["fields"][0] = note_json["front_reverse"]
reverse_card["fields"][1] = note_json["back_reverse"]
reverse_card["fields"][2] = first_guid
reverse_card["fields"][3] =  note_json["reference"]
reverse_card["guid"]      =  second_guid


file_json['notes'] << front_card
file_json['notes'] << reverse_card

pretty_file = JSON.pretty_generate(file_json)

File.open(options[:file], 'w') do |file|
  file.write(pretty_file)
end

puts "Note added!"
