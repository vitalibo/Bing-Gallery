class BingGallery < Formula
  include Language::Python::Virtualenv

  desc "Command-line tool for change desktop picture based on Bing image archive"
  homepage "https://github.com/vitalibo/bing-gallery/"
  url "https://github.com/vitalibo/bing-gallery/releases/download/0.4.0/bing_gallery-0.4.0.tar.gz"
  sha256 "5d1088fa8825e87cb3f1c15637439c310ef073a5bf41e575956fda72e17ec58c"
  license "MIT License"

  depends_on "python@3.12"

  def install
    virtualenv_install_with_resources
  end
end
