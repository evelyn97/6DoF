#!/usr/bin/env ruby

require 'json'
require 'rest-client'
require 'dimensions'

NYPL_API_TOKEN = "b1wnsb6c2edaxo6b"
NYPL_AUTH = "Token token=\"#{NYPL_API_TOKEN}\""
NYPL_ENDPOINT = "http://api.repo.nypl.org/api/v1/items"

if NYPL_API_TOKEN.nil?
  abort("You must set an NYPL_API_TOKEN environment variable with your token from http://api.repo.nypl.org/")
end

stereo_metadata = JSON.parse(RestClient.get("http://stereo.nypl.org/view/#{ARGV[0]}.json"))

unless stereo_metadata['external_id'] == 0
  abort('Image must be from NYPL collections.')
end

gif_url = stereo_metadata['aws_url']
`wget -nc -O #{ARGV[0]}_gif.jpg '#{gif_url}'`

gifName = ARGV[0] + '_gif.jpg'
size = File.size(gifName)
if size.nil?
  puts image_captures.to_json
  abort("Low-quality cropping for #{ARGV[0]}")
end
  
digital_id = stereo_metadata['digitalid'].upcase
image_id = JSON.parse(RestClient.get("#{NYPL_ENDPOINT}/local_image_id/#{digital_id}", :Authorization => NYPL_AUTH))
image_uuid = image_id['nyplAPI']['response']['uuid']
image_captures = JSON.parse(RestClient.get("#{NYPL_ENDPOINT}/#{image_uuid}", :Authorization => NYPL_AUTH))

matching_captures = image_captures['nyplAPI']['response']['capture'].select{|c| c['imageID'].upcase == digital_id}

if matching_captures && matching_captures.length > 0
  # capture_uuid = matching_captures[0]['uuid']
  # capture_details = JSON.parse(RestClient.get("#{NYPL_ENDPOINT}/item_details/#{capture_uuid}", :Authorization => NYPL_AUTH))
  highres_url = matching_captures[0]['highResLink']
  lowres_url = stereo_metadata['url']

  if highres_url.nil? || highres_url.empty?
    puts image_captures.to_json
    abort("No highResLink for #{digital_id}")
  end

  # download images
  # $stdout.puts "Downloading images..."
  `wget -nc -O #{ARGV[0]}.jpg '#{lowres_url}'`
  `wget -nc -O /Users/ying/documents/uw/Junior-quarter4/lab/tif/#{ARGV[0]}.tif '#{highres_url}'`

  # calculate the crop for the original image using multiscale template matching
  # $stdout.puts "Calculating crop..."
  crop_params = `/Users/ying/documents/uw/Junior-quarter4/lab/torch-warp-master/template_match_multiscale.py --template #{ARGV[0]}.jpg --image /Users/ying/documents/uw/Junior-quarter4/lab/tif/#{ARGV[0]}.tif`.chomp
  $stdout.puts crop_params
  # apply the crop
  `convert /Users/ying/documents/uw/Junior-quarter4/lab/tif/#{ARGV[0]}.tif -crop #{crop_params} +repage #{ARGV[0]}_cropped.tif`

  # calculate dimensions
  lowres_dims = Dimensions.dimensions("#{ARGV[0]}.jpg")
  highres_dims = Dimensions.dimensions("#{ARGV[0]}_cropped.tif")

  # calculate scaling
  x_scale = highres_dims[0].to_f / lowres_dims[0].to_f
  y_scale = highres_dims[1].to_f / lowres_dims[1].to_f

  # calculate scaled dimensions
  cropped_width = ARGV[5].to_i * x_scale
  cropped_height = ARGV[6].to_i * y_scale
  x1 = ARGV[1].to_i * x_scale # x1 on cropped tif correlating to low res
  x2 = ARGV[2].to_i * x_scale
  y1 = ARGV[3].to_i * y_scale
  y2 = ARGV[4].to_i * y_scale

  # store the metadata
  File.open("/Users/ying/documents/uw/Junior-quarter4/lab/meta/meta_#{ARGV[0]}.txt", 'w+') {|f| f.write(stereo_metadata) }

  # store the url
  # File.open("/Users/ying/documents/uw/Junior-quarter4/lab/url/hiurl_#{ARGV[0]}.txt", 'w+') {|f| f.write(highres_url) }

  # use the scaled dimensions to split the cropped original into the component images
  # $stdout.puts "Cropping image..."

  # create directory for sotring cropped images
  # Dir.mkdir("/Users/ying/documents/uw/Junior-quarter4/lab/#{ARGV[0]}")
  #   unless File.exists?("/Users/ying/documents/uw/Junior-quarter4/lab/#{ARGV[0]}")

  
  # Dir.chdir "/Users/ying/documents/uw/Junior-quarter4/lab/#{ARGV[0]}"# # change directory

  `convert #{ARGV[0]}_cropped.tif -crop #{cropped_width}x#{cropped_height}+#{x1}+#{y1} +repage /Users/ying/documents/uw/Junior-quarter4/lab/cons/#{ARGV[0]}/con-imL.png`

  `convert #{ARGV[0]}_cropped.tif -crop #{cropped_width}x#{cropped_height}+#{x2}+#{y2} +repage /Users/ying/documents/uw/Junior-quarter4/lab/cons/#{ARGV[0]}/con-imR.png`

  $stdout.puts lowres_dims
  $stdout.puts highres_dims
  $stdout.puts highres_url
else
  puts image_captures.to_json
  abort("No matching captures for #{digital_id}")
end
