// https://observablehq.com/@florencewallis/along@58
import define1 from "./12467aabdea216dd@1588.js";
import define2 from "./834f195f1a2b5c8b@180.js";

export default function define(runtime, observer) {
  const main = runtime.module();
  main.variable(observer()).define(["md"], function(md){return(
md`# Along`
)});
  main.variable(observer()).define(["myP","rs"], function(myP,rs){return(
myP, rs`Like being knit together 
                as though to create soil: 
                        creeping, quick, 
                 the silver of me darted, 
                       grew in moonlight;
      and this is how I learned to drink. 
<br>

I drank when it was no time to drink
lava hardening and a fine ash
the tiling blue and white, triangles, squares,<br>

and the arches and collapses,
           the headlands
                          and the stacks of stone;
                my childhood in striation.<br>


 Like (being knit together | being crushed down in my chest, )
                (as though to create soil: |to create diamonds:)
                 (creeping, quick, | so hot, this learning, this forming -)
                ( the silver of me darted, | the gold of me melted,)
                       (grew in moonlight; | fell dripping around;)
(and this is how I learned to drink. | and this is how I learned to walk.)<br>

I walked out into the leaves
and the spaces below the leaves
and the falling through the spaces<br>

    and the arches and collapses, a process 
                                       not separate 
                        from this moment 
of my foot finding its landing.
<br>
                       I went to touch the flower 
                       and a few raindrops fell. 
                       This is how I knew that it was not for me.<br> 

 Like (being knit together | being crushed down in my chest, | being eroded, like a softening in my skull,)
                (as though to create soil: |to create diamonds:|as though to rot)
                  (creeping, quick, | so hot, this learning, this forming -| into the layered atmosphere)
                ( the silver of me darted, | the gold of me melted,|   the copper of me flew out )
                       (grew in moonlight; | fell dripping around;| along the cliffs,)
(and this is how I learned to drink. | and this is how I learned to walk.| and this is how I learned to loosen.  )<br>

    My loosenings, my letting-goes 
     were never to dust. I had a hard time 
     letting go. My trees piled up<br>

and now there are arrows
        in the knobbed, broken 
      sticks scattering these paths
 that point in both directions at once<br>

                       I went to change the twigs
                       but the light spun around.
                       This is how I knew the compass.   <br>

 Like (being knit together | being crushed down in my chest, | being eroded, like a softening in my skull, | silver on shells -)
                (as though to create soil: |to create diamonds:|as though to rot|hesitant and pale, this reaching back )
                  (creeping, quick, | so hot, this learning, this forming -| into the layered atmosphere| along the old paths.)
                ( the silver of me darted, | the gold of me melted,|   the copper of me flew out |The salt of me caught,)
                       (grew in moonlight; | fell dripping around;| along the cliffs,|connected; the crust and cool of it)
(and this is how I learned to drink. | and this is how I learned to walk.| and this is how I learned to loosen.  |and this is how I learned to wane.)<br>

Sun’s yellow to stars’ shine -
the spores of the night parsing
the sodium of  sea air,
<br>
and the tiny and endless tides
   pulling the cells of our selfhood.
     I began the unloosening;
        spoken and spilling
<br>
		I have been a word among letters
		held loose on the tongue -
		and this is how I knew the song.
<br>
 Like (being knit together | being crushed down in my chest, | being eroded, like a softening in my skull, | silver on shells -|mycelium regrowing)
                (as though to create soil: |to create diamonds:|as though to rot|hesitant and pale, this reaching back |in the longing held by the dark:)
                  (creeping, quick, | so hot, this learning, this forming -| into the layered atmosphere| along the old paths.|softening, slowing,)
                ( the silver of me darted, | the gold of me melted,|   the copper of me flew out |The salt of me caught,|the iron of me held, )
                       (grew in moonlight; | fell dripping around;| along the cliffs,|connected; the crust and cool of it|and released, rusted the sharp-edged dream)
(and this is how I learned to drink. | and this is how I learned to walk.| and this is how I learned to loosen.  |and this is how I learned to wane.|and this is how I learned to sleep.)<br>

I slept in composition
as though song’s arch swept across 
the sighed length of me
<br>
and unknit time
    into a polyphonic glittering -
       these intricacies that find an opening
           into my decomposed moment.

<br>
 Like (being knit together | being crushed down in my chest, | root systems bared of earth |being eroded, like a softening in my skull,|silver on shells -|mycelium regrowing)
                (as though to create soil: |to create diamonds:|as though to rot|hesitant and pale, this reaching back |in the longing held by the dark:| the spine and ribs of them,)
                 (creeping, quick, | so hot, this learning, this forming -| into the layered atmosphere| their branching finitude -|into the layered atmosphere| along the old paths.|softening, slowing,)
                ( the silver of me darted, | the gold of me melted,|   the copper of me flew out | the phosphorus of me burned out |The salt of me caught,|the iron of me held,  )
                       (grew in moonlight; | fell dripping around;| along the cliffs,| along my bones:|connected; the crust and cool of it|and released, rusted the sharp-edged dream)
(and this is how I learned to drink. | and this is how I learned to walk.| and this is how I learned to loosen.  | and this is how I learned to unmake.|and this is how I learned to wane.|and this is how I learned to sleep.)
 <br>
I know what draws the wick,
hear the writhing pale rings:
nerves with gills on their underside<br>

 and the radiance that repeats time:
     the salts of its passing,
     the waxing 
        and glowing of our passing. <br>

`
)});
  const child1 = runtime.module(define1);
  main.import("rs", child1);
  const child2 = runtime.module(define2);
  main.import("pulse", child2);
  main.variable(observer("myP")).define("myP", ["pulse"], function(pulse){return(
pulse(3500)
)});
  return main;
}
