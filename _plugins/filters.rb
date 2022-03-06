module Jekyll
  module EntryFilters
    SLUG_MODE = 'latin'.freeze

    def entry_link(input, current_letter)
      slug = entry_slug(input)
      letter = slug[0].upcase
      if letter == current_letter
        "##{slug}"
      else
        # TODO: use {{link}} or something to generate this /<letter>.html
        "/#{letter}.html##{slug}"
      end
    end

    def entry_slug(input)
      Jekyll::Utils.slugify(input, mode: SLUG_MODE)
    end
  end
end

Liquid::Template.register_filter(Jekyll::EntryFilters)