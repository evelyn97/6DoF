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
if size==0 
  # puts image_captures.to_json
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
  `wget -nc -O /projects/grail/6DOFnb/NYPL_new/#{ARGV[0]}.jpg '#{lowres_url}'`
  `wget -nc -O /projects/grail/6DOFnb/NYPL_new/tif/#{ARGV[0]}.tif '#{highres_url}'`

  # calculate the crop for the original image using multiscale template matching
  # $stdout.puts "Calculating crop..."
  crop_params = `./template_match_multiscale.py --template /projects/grail/6DOFnb/NYPL_new/#{ARGV[0]}.jpg --image /projects/grail/6DOFnb/NYPL_new/tif/#{ARGV[0]}.tif`.chomp

  # apply the crop
  `convert /projects/grail/6DOFnb/NYPL_new/tif/#{ARGV[0]}.tif -crop #{crop_params} +repage /projects/grail/6DOFnb/NYPL_new/#{ARGV[0]}_cropped.tif`

  # calculate dimensions
  lowres_dims = Dimensions.dimensions("/projects/grail/6DOFnb/NYPL_new/#{ARGV[0]}.jpg")
  highres_dims = Dimensions.dimensions("/projects/grail/6DOFnb/NYPL_new/#{ARGV[0]}_cropped.tif")

  # calculate scaling
  x_scale = highres_dims[0].to_f / lowres_dims[0].to_f
  y_scale = highres_dims[1].to_f / lowres_dims[1].to_f

  # calculate scaled dimensions
  cropped_width = stereo_metadata['width'] * x_scale
  cropped_height = stereo_metadata['height'] * y_scale
  x1 = stereo_metadata['x1'] * x_scale
  x2 = stereo_metadata['x2'] * x_scale
  y1 = stereo_metadata['y1'] * y_scale
  y2 = stereo_metadata['y2'] * y_scale

  # store the metadata
  File.open("/projects/grail/6DOFnb/NYPL_new/meta/meta_#{ARGV[0]}.json","w") do |f|
    f.write(stereo_metadata.to_json)
  end
  # File.open("/projects/grail/6DOFnb/NYPL/meta/meta_#{ARGV[0]}.txt", 'w+') {|f| f.write(stereo_metadata) }

  # store the url
  # File.open("/Users/ying/documents/uw/Junior-quarter4/lab/url/hiurl_#{ARGV[0]}.txt", 'w+') {|f| f.write(highres_url) }

  # use the scaled dimensions to split the cropped original into the component images
  # $stdout.puts "Cropping image..."

  # create directory for sotring cropped images
  # Dir.mkdir("/Users/ying/documents/uw/Junior-quarter4/lab/#{ARGV[0]}")
  #   unless File.exists?("/Users/ying/documents/uw/Junior-quarter4/lab/#{ARGV[0]}")

  
  # Dir.chdir "/Users/ying/documents/uw/Junior-quarter4/lab/#{ARGV[0]}"# # change directory

  `convert /projects/grail/6DOFnb/NYPL_new/#{ARGV[0]}_cropped.tif -crop #{cropped_width}x#{cropped_height}+#{x1}+#{y1} +repage /projects/grail/6DOFnb/NYPL_new/cropped/#{ARGV[0]}/imL.png`

  `convert /projects/grail/6DOFnb/NYPL_new/#{ARGV[0]}_cropped.tif -crop #{cropped_width}x#{cropped_height}+#{x2}+#{y2} +repage /projects/grail/6DOFnb/NYPL_new/cropped/#{ARGV[0]}/imR.png`

  $stdout.puts highres_url
else
  puts image_captures.to_json
  abort("No matching captures for #{digital_id}")
end
